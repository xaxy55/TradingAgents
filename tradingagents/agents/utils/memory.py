import chromadb
from chromadb.config import Settings
from openai import OpenAI
import time
import random

from tradingagents.utils.context_budget import truncate_text_middle


class FinancialSituationMemory:
    def __init__(self, name, config):
        self.config = config
        self.llm_provider = config.get("llm_provider", "openai").lower()
        self.max_retries = 3
        self.base_delay = 1  # seconds
        
        if self.llm_provider == "google":
            # Use Google embeddings via LangChain
            try:
                from langchain_google_genai import GoogleGenerativeAIEmbeddings
                self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            except ImportError:
                raise ImportError("langchain-google-genai is required for Google embeddings. Install with: pip install langchain-google-genai")
            self.client = None
        else:
            # Use OpenAI embeddings
            if self.llm_provider == "ollama":
                # Ollama - local inference, use dummy API key
                self.embedding = "nomic-embed-text"
                self.client = OpenAI(base_url=config["backend_url"], api_key="ollama")
            else:
                # OpenAI or OpenRouter - will use OPENAI_API_KEY or OPENROUTER_API_KEY env var
                self.embedding = "text-embedding-3-small"
                self.client = OpenAI(base_url=config["backend_url"])
            self.embeddings = None
        
        self.chroma_client = chromadb.Client(Settings(allow_reset=True))
        self.situation_collection = self.chroma_client.get_or_create_collection(name=name)

    def get_embedding(self, text):
        """Get embedding for a text using the configured provider with retry logic"""

        # Embedding endpoints have their own input limits; keep this conservative.
        max_embed_tokens = 6000
        try:
            # Allow overriding via config if present.
            max_embed_tokens = int(getattr(self, "config", {}).get("embedding_max_input_tokens", max_embed_tokens))
        except Exception:
            pass

        text = truncate_text_middle(text, max_embed_tokens)
        
        for attempt in range(self.max_retries):
            try:
                if self.llm_provider == "google":
                    return self.embeddings.embed_query(text)
                else:
                    response = self.client.embeddings.create(
                        model=self.embedding, input=text
                    )
                    return response.data[0].embedding
            except Exception as e:
                if "429" in str(e) or "rate" in str(e).lower():
                    if attempt < self.max_retries - 1:
                        delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                        print(f"Rate limited. Retrying in {delay:.1f}s... (Attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(delay)
                    else:
                        raise
                else:
                    raise

    def add_situations(self, situations_and_advice):
        """Add financial situations and their corresponding advice. Parameter is a list of tuples (situation, rec)"""

        situations = []
        advice = []
        ids = []
        embeddings = []

        offset = self.situation_collection.count()

        for i, (situation, recommendation) in enumerate(situations_and_advice):
            situations.append(situation)
            advice.append(recommendation)
            ids.append(str(offset + i))
            embeddings.append(self.get_embedding(situation))

        self.situation_collection.add(
            documents=situations,
            metadatas=[{"recommendation": rec} for rec in advice],
            embeddings=embeddings,
            ids=ids,
        )

    def get_memories(self, current_situation, n_matches=1):
        """Find matching recommendations using OpenAI embeddings"""
        query_embedding = self.get_embedding(current_situation)

        results = self.situation_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_matches,
            include=["metadatas", "documents", "distances"],
        )

        matched_results = []
        for i in range(len(results["documents"][0])):
            matched_results.append(
                {
                    "matched_situation": results["documents"][0][i],
                    "recommendation": results["metadatas"][0][i]["recommendation"],
                    "similarity_score": 1 - results["distances"][0][i],
                }
            )

        return matched_results


if __name__ == "__main__":
    # Example usage
    from tradingagents.default_config import DEFAULT_CONFIG
    
    config = DEFAULT_CONFIG.copy()
    matcher = FinancialSituationMemory("test_memory", config)

    # Example data
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # Add the example situations and recommendations
    matcher.add_situations(example_data)

    # Example query
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors 
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
