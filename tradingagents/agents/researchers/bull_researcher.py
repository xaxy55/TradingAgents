from langchain_core.messages import AIMessage
import time
import json


def create_bull_researcher(llm, memory):
    def bull_node(state) -> dict:
        investment_debate_state = state["investment_debate_state"]
        asset_type = state.get("asset_type", "stock")
        history = investment_debate_state.get("history", "")
        bull_history = investment_debate_state.get("bull_history", "")

        current_response = investment_debate_state.get("current_response", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        # Adjust prompt based on asset type
        if asset_type == "cryptocurrency":
            asset_focus = "cryptocurrency"
            additional_guidance = """
**CRYPTOCURRENCY-SPECIFIC BULL FACTORS:**
- Adoption & Network Growth: Increasing user base, transaction volume, and real-world use cases
- Technology Innovation: Unique technical features, scalability improvements, or ecosystem development
- Institutional Interest: Major companies or institutions investing or integrating the cryptocurrency
- Regulatory Clarity: Positive regulatory developments or legal recognition
- Market Position: Strong position relative to competitors in its category
- Community & Development: Active developer community and ongoing project improvements
- Macro Environment: Favorable conditions for risk assets or specific crypto catalysts"""
        else:
            asset_focus = "stock"
            additional_guidance = ""

        prompt = f"""You are a Bull Analyst advocating for investing in the {asset_focus}. Your task is to build a strong, evidence-based case emphasizing growth potential, competitive advantages, and positive market indicators. Leverage the provided research and data to address concerns and counter bearish arguments effectively.

Key points to focus on:
- Growth Potential: Highlight market opportunities, projected growth, and scalability.
- Competitive Advantages: Emphasize unique factors like technology, positioning, or network effects.
- Positive Indicators: Use technical analysis, sentiment trends, and recent positive news as evidence.
- Bear Counterpoints: Critically analyze the bear argument with specific data and sound reasoning, addressing concerns thoroughly and showing why the bull perspective holds stronger merit.
- Engagement: Present your argument in a conversational style, engaging directly with the bear analyst's points and debating effectively rather than just listing data.{additional_guidance}

Resources available:
Market research report: {market_research_report}
Social media sentiment report: {sentiment_report}
Latest world affairs news: {news_report}
{"Company fundamentals report" if asset_type == "stock" else "Project analysis"}: {fundamentals_report}
Conversation history of the debate: {history}
Last bear argument: {current_response}
Reflections from similar situations and lessons learned: {past_memory_str}
Use this information to deliver a compelling bull argument, refute the bear's concerns, and engage in a dynamic debate that demonstrates the strengths of the bull position. You must also address reflections and learn from lessons and mistakes you made in the past.
"""

        response = llm.invoke(prompt)

        argument = f"Bull Analyst: {response.content}"

        new_investment_debate_state = {
            "history": history + "\n" + argument,
            "bull_history": bull_history + "\n" + argument,
            "bear_history": investment_debate_state.get("bear_history", ""),
            "current_response": argument,
            "count": investment_debate_state["count"] + 1,
        }

        return {"investment_debate_state": new_investment_debate_state}

    return bull_node
