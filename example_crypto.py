"""
Example: Using TradingAgents with Cryptocurrency

This example demonstrates how to use TradingAgents to analyze
cryptocurrencies like Bitcoin and Ethereum.
"""

import copy
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()

def analyze_crypto(symbol, date):
    """
    Analyze a cryptocurrency using TradingAgents.
    
    Args:
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        date: Analysis date in YYYY-MM-DD format
    """
    print(f"\n{'='*60}")
    print(f"Analyzing {symbol} on {date}")
    print('='*60)
    
    # Create configuration for crypto analysis
    config = copy.deepcopy(DEFAULT_CONFIG)
    config["deep_think_llm"] = "gpt-4o-mini"
    config["quick_think_llm"] = "gpt-4o-mini"
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1
    
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
        print("  - OPENAI_API_KEY")
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
    
    # Example 1: Analyze Bitcoin
    print("\n\n" + "="*60)
    print("EXAMPLE 1: Bitcoin (BTC) Analysis")
    print("="*60)
    
    # Note: Using a past date for reproducibility
    analyze_crypto("BTC", "2024-05-10")
    
    # Example 2: Analyze Ethereum
    print("\n\n" + "="*60)
    print("EXAMPLE 2: Ethereum (ETH) Analysis")
    print("="*60)
    
    analyze_crypto("ETH", "2024-05-10")
    
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
    import os
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  WARNING: OPENAI_API_KEY not set!")
        print("Please set your OpenAI API key to run this example:")
        print("  export OPENAI_API_KEY=your_key_here")
        print()
    
    if not os.getenv("ALPHA_VANTAGE_API_KEY"):
        print("\n⚠️  WARNING: ALPHA_VANTAGE_API_KEY not set!")
        print("Please set your Alpha Vantage API key to run this example:")
        print("  export ALPHA_VANTAGE_API_KEY=your_key_here")
        print("\nYou can get a free API key at:")
        print("  https://www.alphavantage.co/support/#api-key")
        print()
    
    if os.getenv("OPENAI_API_KEY") and os.getenv("ALPHA_VANTAGE_API_KEY"):
        main()
    else:
        print("\n❌ Cannot run example without API keys.")
        print("Please set the required environment variables and try again.")
        print()
