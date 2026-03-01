"""
Example: Using TradingAgents with Cryptocurrency and Ollama

This example demonstrates how to use TradingAgents with Ollama (local LLM)
to analyze cryptocurrencies like Bitcoin.

Prerequisites:
1. Install Ollama: https://ollama.ai
2. Pull required models:
   ollama pull llama3.1
   ollama pull qwen3
3. Start Ollama server (usually starts automatically)
4. Set ALPHA_VANTAGE_API_KEY environment variable
"""

import copy
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import os
import sys

# Load environment variables (API keys)
load_dotenv()


def check_ollama_available():
    """Check if Ollama is running and accessible."""
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            print(f"✓ Ollama is running with {len(models)} model(s): {', '.join(model_names[:3])}")
            return True, model_names
        else:
            print("✗ Ollama server responded but with an error")
            return False, []
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Ollama at http://localhost:11434")
        print("  Please make sure Ollama is installed and running")
        print("  Visit: https://ollama.ai")
        return False, []
    except Exception as e:
        print(f"✗ Error checking Ollama: {e}")
        return False, []


def analyze_crypto_with_ollama(symbol, date, deep_model="llama3.1", quick_model="llama3.1"):
    """
    Analyze a cryptocurrency using TradingAgents with Ollama.
    
    Args:
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        date: Analysis date in YYYY-MM-DD format
        deep_model: Ollama model for deep thinking (e.g., 'llama3.1', 'qwen3')
        quick_model: Ollama model for quick thinking (e.g., 'llama3.1', 'llama3.2')
    """
    print(f"\n{'='*70}")
    print(f"Analyzing {symbol} on {date} with Ollama")
    print('='*70)
    
    # Create configuration for crypto analysis with Ollama
    config = copy.deepcopy(DEFAULT_CONFIG)
    
    # Configure Ollama as the LLM provider
    config["llm_provider"] = "ollama"
    config["backend_url"] = "http://localhost:11434/v1"
    config["deep_think_llm"] = deep_model
    config["quick_think_llm"] = quick_model
    
    # Configure analysis depth (use shallow depth for faster local execution)
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1
    
    # Cryptocurrency-specific settings
    config["crypto_settings"]["default_market"] = "USD"
    config["crypto_settings"]["default_interval"] = "60min"
    
    # Configure data vendors for crypto
    config["data_vendors"]["cryptocurrency_data"] = "alpha_vantage"
    
    # Initialize TradingAgentsGraph with Ollama
    print(f"\nInitializing TradingAgents with Ollama for {symbol}...")
    print(f"Deep thinking model: {config['deep_think_llm']}")
    print(f"Quick thinking model: {config['quick_think_llm']}")
    print(f"Note: Using local Ollama models - this may be slower but runs entirely on your machine")
    
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Run analysis
    print(f"\nRunning multi-agent analysis for {symbol}...")
    print("This will use Ollama for:")
    print("  - Market Analyst (technical analysis)")
    print("  - News Analyst (sentiment from news)")
    print("  - Research Team (bull/bear debate)")
    print("  - Risk Management")
    print("  - Portfolio Manager (final decision)")
    print()
    
    try:
        _, decision = ta.propagate(symbol, date)
        
        print(f"\n{'='*70}")
        print(f"Analysis Complete for {symbol} with Ollama")
        print('='*70)
        print("\nFinal Trading Decision:")
        print(decision)
        print()
        
        return decision
        
    except Exception as e:
        print(f"\n✗ Error during analysis: {e}")
        print("\nNote: Make sure you have:")
        print("  1. Ollama installed and running (https://ollama.ai)")
        print(f"  2. Models pulled: ollama pull {deep_model}")
        print("  3. ALPHA_VANTAGE_API_KEY environment variable set")
        import traceback
        traceback.print_exc()
        return None


def main():
    """
    Main function demonstrating cryptocurrency analysis with Ollama.
    """
    print("\n" + "="*70)
    print("TradingAgents Cryptocurrency Analysis with Ollama")
    print("="*70)
    print("\nThis example demonstrates analyzing Bitcoin (BTC)")
    print("using Ollama as the local LLM provider.")
    
    # Check if Ollama is available
    print("\n" + "="*70)
    print("Checking Ollama Availability")
    print("="*70)
    ollama_available, available_models = check_ollama_available()
    
    if not ollama_available:
        print("\n❌ Cannot proceed without Ollama.")
        print("\nTo install Ollama:")
        print("  1. Visit https://ollama.ai")
        print("  2. Download and install for your platform")
        print("  3. Run: ollama pull llama3.1")
        print("  4. The server should start automatically")
        return
    
    # Check ALPHA_VANTAGE_API_KEY
    if not os.getenv("ALPHA_VANTAGE_API_KEY"):
        print("\n⚠️  WARNING: ALPHA_VANTAGE_API_KEY not set!")
        print("Please set your Alpha Vantage API key to run this example:")
        print("  export ALPHA_VANTAGE_API_KEY=your_key_here")
        print("\nYou can get a free API key at:")
        print("  https://www.alphavantage.co/support/#api-key")
        print("\n❌ Cannot run example without API key.")
        return
    
    # Select models to use
    print("\n" + "="*70)
    print("Model Configuration")
    print("="*70)
    
    # Check if recommended models are available
    deep_model = "llama3.1"
    quick_model = "llama3.1"
    
    if available_models:
        # Use llama3.1 or qwen3 for deep thinking if available
        if any("llama3.1" in m for m in available_models):
            deep_model = "llama3.1"
        elif any("qwen3" in m for m in available_models):
            deep_model = "qwen3"
        elif available_models:
            deep_model = available_models[0].split(":")[0]
        
        # Use llama3.1 or llama3.2 for quick thinking if available
        if any("llama3.1" in m for m in available_models):
            quick_model = "llama3.1"
        elif any("llama3.2" in m for m in available_models):
            quick_model = "llama3.2"
        elif available_models:
            quick_model = available_models[0].split(":")[0]
    
    print(f"Using models:")
    print(f"  Deep thinking: {deep_model}")
    print(f"  Quick thinking: {quick_model}")
    
    if not available_models or not any("llama3" in m or "qwen3" in m for m in available_models):
        print("\n⚠️  Recommended models not found!")
        print("For best results, pull recommended models:")
        print("  ollama pull llama3.1")
        print("  ollama pull qwen3")
        print("\nProceeding with available models...\n")
    
    # Example: Analyze Bitcoin with Ollama
    print("\n" + "="*70)
    print("EXAMPLE: Bitcoin (BTC) Analysis with Ollama")
    print("="*70)
    print("\nNote: This example uses local LLM inference, which may take longer")
    print("than cloud-based APIs, but runs entirely on your machine.")
    
    analyze_crypto_with_ollama("BTC", "2024-05-10", deep_model, quick_model)
    
    # Summary
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    print("\n✓ Successfully tested TradingAgents with:")
    print("  • Cryptocurrency: Bitcoin (BTC)")
    print("  • LLM Provider: Ollama (local)")
    print("  • Models: Local open-source models")
    print("\nBenefits of using Ollama:")
    print("  • Complete privacy - runs entirely on your machine")
    print("  • No API costs - free to use")
    print("  • Offline capable - no internet required (except for market data)")
    print("  • Open source models - full transparency")
    print("\nYou can analyze any cryptocurrency with Ollama:")
    print("  • Bitcoin (BTC)")
    print("  • Ethereum (ETH)")
    print("  • And 30+ other major cryptocurrencies")
    print("\nFor more information, see CRYPTOCURRENCY.md")
    print()


if __name__ == "__main__":
    # Add requests to dependencies check
    try:
        import requests
        # Access an attribute to ensure the import is considered "used"
        _ = requests.__version__
    except ImportError:
        print("\n⚠️  Missing 'requests' library!")
        print("Install it with: pip install requests")
        sys.exit(1)
    
    main()
