"""
Example: Using TradingAgents with Cryptocurrency

This example demonstrates how to use TradingAgents to analyze
cryptocurrencies like Bitcoin and Ethereum.
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import os
import time

# Load environment variables (API keys)
load_dotenv()

def analyze_crypto(symbol, date, llm_provider="openai"):
    """
    Analyze a cryptocurrency using TradingAgents.
    
    Args:
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        date: Analysis date in YYYY-MM-DD format
        llm_provider: LLM provider to use - "openai" or "google" (default: "openai")
    """
    print(f"\n{'='*60}")
    print(f"Analyzing {symbol} on {date} using {llm_provider.upper()}")
    print('='*60)
    
    # Create configuration for crypto analysis
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = llm_provider.lower()
    
    if llm_provider.lower() == "openai":
        config["deep_think_llm"] = "gpt-4o-mini"
        config["quick_think_llm"] = "gpt-4o-mini"
    elif llm_provider.lower() == "google":
        config["deep_think_llm"] = "gemini-2.0-flash"
        config["quick_think_llm"] = "gemini-2.0-flash"
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}. Use 'openai' or 'google'.")
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1
    
    # Add delay between API calls to avoid rate limiting (especially important for free tier Google API)
    config["api_call_delay"] = 1  # seconds between API calls
    
    # Cryptocurrency-specific settings
    config["crypto_settings"]["default_market"] = "USD"
    config["crypto_settings"]["default_interval"] = "60min"
    
    # Configure data vendors for crypto
    config["data_vendors"]["cryptocurrency_data"] = "alpha_vantage"
    
    # Initialize TradingAgentsGraph
    print(f"\nInitializing TradingAgents for {symbol}...")
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Run analysis
    print(f"\nRunning multi-agent analysis for {symbol}...")
    print("This will use:")
    print("  - Market Analyst (technical analysis)")
    print("  - News Analyst (sentiment from news)")
    print("  - Research Team (bull/bear debate)")
    print("  - Risk Management Team")
    print("  - Portfolio Manager (final decision)")
    print()
    
    try:
        _, decision = ta.propagate(symbol, date)
        
        print(f"\n{'='*60}")
        print(f"Analysis Complete for {symbol}")
        print('='*60)
        print("\nFinal Trading Decision:")
        print(decision)
        print()
        
        return decision
        
    except Exception as e:
        print(f"\n✗ Error during analysis: {e}")
        print("\nNote: Make sure you have set the following environment variables:")
        if llm_provider.lower() == "openai":
            print("  - OPENAI_API_KEY")
        elif llm_provider.lower() == "google":
            print("  - GOOGLE_API_KEY")
        print("  - ALPHA_VANTAGE_API_KEY")
        return None


def main():
    """
    Main function demonstrating cryptocurrency analysis.
    """
    print("\n" + "="*60)
    print("TradingAgents Cryptocurrency Analysis Example")
    print("="*60)
    print("\nThis example demonstrates analyzing cryptocurrencies")
    print("using the TradingAgents multi-agent framework.")
    print("\nSupported LLM Providers:")
    print("  - OpenAI (GPT-4o-mini)")
    print("  - Google (Gemini 2.0 Flash)")
    
    # Determine which LLM provider to use based on environment
    llm_provider = "openai"
    if os.getenv("GOOGLE_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        llm_provider = "google"
    elif os.getenv("GOOGLE_API_KEY"):
        # If both are available, you can change this preference
        llm_provider = "google"
    
    # Example 1: Analyze Bitcoin
    print("\n\n" + "="*60)
    print("EXAMPLE 1: Bitcoin (BTC) Analysis with " + llm_provider.upper())
    print("="*60)
    
    # Note: Using a past date for reproducibility
    btc_decision = analyze_crypto("BTC", "2024-05-10", llm_provider)
    
    # Add delay between analyses to avoid rate limiting
    print("\nWaiting 5 seconds before next analysis...")
    time.sleep(5)
    
    # Example 2: Analyze Ethereum
    print("\n\n" + "="*60)
    print("EXAMPLE 2: Ethereum (ETH) Analysis with " + llm_provider.upper())
    print("="*60)
    
    eth_decision = analyze_crypto("ETH", "2024-05-10", llm_provider)
    
    # Summary
    print("\n\n" + "="*60)
    print("Summary")
    print("="*60)
    print("\nYou can now use TradingAgents to analyze:")
    print("  • Stocks (AAPL, GOOGL, NVDA, etc.)")
    print("  • Cryptocurrencies (BTC, ETH, SOL, etc.)")
    print("\nThe framework automatically detects the asset type")
    print("and routes to the appropriate data sources.")
    print("\nFor more information, see README.md")
    print()


if __name__ == "__main__":
    # Check if API keys are set
    has_openai = os.getenv("OPENAI_API_KEY")
    has_google = os.getenv("GOOGLE_API_KEY")
    has_alpha_vantage = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    if not has_openai and not has_google:
        print("\n⚠️  WARNING: No LLM API keys set!")
        print("\nPlease set at least ONE of the following:")
        print("\n  Option 1: Google Gemini API Key")
        print("    export GOOGLE_API_KEY=your_google_key_here")
        print("    You can get a free Google API key at:")
        print("    https://aistudio.google.com/app/apikey")
        print("\n  Option 2: OpenAI API Key")
        print("    export OPENAI_API_KEY=your_openai_key_here")
        print()
    
    if not has_alpha_vantage:
        print("\n⚠️  WARNING: ALPHA_VANTAGE_API_KEY not set!")
        print("Please set your Alpha Vantage API key to run this example:")
        print("  export ALPHA_VANTAGE_API_KEY=your_key_here")
        print("\nYou can get a free API key at:")
        print("  https://www.alphavantage.co/support/#api-key")
        print()
    
    if (has_openai or has_google) and has_alpha_vantage:
        main()
    else:
        print("\n❌ Cannot run example without required API keys.")
        print("Please set the required environment variables and try again.")
        print()
