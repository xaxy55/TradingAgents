"""
Example: Using TradingAgents with Cryptocurrency and Google Gemini

This example demonstrates how to use TradingAgents with Google Gemini LLM
to analyze cryptocurrencies like Bitcoin and Ethereum.
"""

import copy
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import os

# Load environment variables (API keys)
load_dotenv()

def analyze_crypto_with_gemini(symbol, date):
    """
    Analyze a cryptocurrency using TradingAgents with Google Gemini.
    
    Args:
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        date: Analysis date in YYYY-MM-DD format
    """
    print(f"\n{'='*70}")
    print(f"Analyzing {symbol} on {date} with Google Gemini")
    print('='*70)
    
    # Create configuration for crypto analysis with Google Gemini
    config = copy.deepcopy(DEFAULT_CONFIG)
    
    # Configure Google Gemini as the LLM provider
    config["llm_provider"] = "google"
    config["backend_url"] = "https://generativelanguage.googleapis.com/v1"
    config["deep_think_llm"] = "gemini-2.0-flash"  # For complex reasoning
    config["quick_think_llm"] = "gemini-2.0-flash-lite"  # For fast operations
    
    # Optional: Use other Gemini models
    # config["deep_think_llm"] = "gemini-2.5-pro-preview-06-05"  # Most capable
    # config["quick_think_llm"] = "gemini-2.5-flash-preview-05-20"  # Balanced
    
    # Configure analysis depth
    config["max_debate_rounds"] = 2
    config["max_risk_discuss_rounds"] = 2
    
    # Cryptocurrency-specific settings
    config["crypto_settings"]["default_market"] = "USD"
    config["crypto_settings"]["default_interval"] = "60min"
    
    # Configure data vendors for crypto
    config["data_vendors"]["cryptocurrency_data"] = "alpha_vantage"
    
    # Initialize TradingAgentsGraph with Gemini
    print(f"\nInitializing TradingAgents with Google Gemini for {symbol}...")
    print(f"Deep thinking model: {config['deep_think_llm']}")
    print(f"Quick thinking model: {config['quick_think_llm']}")
    
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Run analysis
    print(f"\nRunning multi-agent analysis for {symbol}...")
    print("This will use Google Gemini for:")
    print("  - Market Analyst (technical analysis)")
    print("  - News Analyst (sentiment from news)")
    print("  - Research Team (bull/bear debate)")
    print("  - Risk Management")
    print("  - Portfolio Manager (final decision)")
    print()
    
    try:
        _, decision = ta.propagate(symbol, date)
        
        print(f"\n{'='*70}")
        print(f"Analysis Complete for {symbol} with Google Gemini")
        print('='*70)
        print("\nFinal Trading Decision:")
        print(decision)
        print()
        
        return decision
        
    except Exception as e:
        print(f"\n✗ Error during analysis: {e}")
        print("\nNote: Make sure you have set the following environment variables:")
        print("  - GOOGLE_API_KEY (for Google Gemini)")
        print("  - ALPHA_VANTAGE_API_KEY (for crypto data)")
        print("\nYou can get a Google API key at:")
        print("  https://ai.google.dev/")
        return None


def main():
    """
    Main function demonstrating cryptocurrency analysis with Google Gemini.
    """
    print("\n" + "="*70)
    print("TradingAgents Cryptocurrency Analysis with Google Gemini")
    print("="*70)
    print("\nThis example demonstrates analyzing cryptocurrencies")
    print("using Google Gemini as the LLM provider.")
    
    # Check API keys
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n⚠️  WARNING: GOOGLE_API_KEY not set!")
        print("Please set your Google API key to run this example:")
        print("  export GOOGLE_API_KEY=your_key_here")
        print("\nYou can get a free API key at:")
        print("  https://ai.google.dev/")
        print()
    
    if not os.getenv("ALPHA_VANTAGE_API_KEY"):
        print("\n⚠️  WARNING: ALPHA_VANTAGE_API_KEY not set!")
        print("Please set your Alpha Vantage API key to run this example:")
        print("  export ALPHA_VANTAGE_API_KEY=your_key_here")
        print("\nYou can get a free API key at:")
        print("  https://www.alphavantage.co/support/#api-key")
        print()
    
    if not (os.getenv("GOOGLE_API_KEY") and os.getenv("ALPHA_VANTAGE_API_KEY")):
        print("\n❌ Cannot run example without API keys.")
        print("Please set the required environment variables and try again.")
        print()
        return
    
    # Example 1: Analyze Bitcoin with Google Gemini
    print("\n\n" + "="*70)
    print("EXAMPLE 1: Bitcoin (BTC) Analysis with Google Gemini")
    print("="*70)
    
    analyze_crypto_with_gemini("BTC", "2024-05-10")
    
    # Example 2: Analyze Ethereum with Google Gemini
    print("\n\n" + "="*70)
    print("EXAMPLE 2: Ethereum (ETH) Analysis with Google Gemini")
    print("="*70)
    
    analyze_crypto_with_gemini("ETH", "2024-05-10")
    
    # Summary
    print("\n\n" + "="*70)
    print("Summary")
    print("="*70)
    print("\nYou can now use TradingAgents with Google Gemini to analyze:")
    print("  • Cryptocurrencies (BTC, ETH, SOL, etc.)")
    print("  • Stocks (AAPL, GOOGL, NVDA, etc.)")
    print("\nSupported LLM Providers:")
    print("  • Google Gemini (gemini-2.0-flash, gemini-2.5-pro, etc.)")
    print("  • OpenAI (gpt-4o, o1, etc.)")
    print("  • Anthropic (claude-3-5-sonnet, claude-4, etc.)")
    print("\nThe framework automatically detects the asset type")
    print("and routes to the appropriate data sources.")
    print("\nFor more information, see CRYPTOCURRENCY.md")
    print()


if __name__ == "__main__":
    main()
