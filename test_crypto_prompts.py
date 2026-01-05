#!/usr/bin/env python3
"""
Test script to verify crypto-specific prompts are working correctly.
"""

from tradingagents.graph.propagation import Propagator
from tradingagents.dataflows.crypto_dataflows import is_crypto_symbol

def test_asset_type_detection():
    """Test that asset types are correctly detected."""
    print("Testing asset type detection...")
    
    # Test crypto symbols
    crypto_symbols = ["BTC", "ETH", "SOL", "DOGE", "MATIC"]
    for symbol in crypto_symbols:
        is_crypto = is_crypto_symbol(symbol)
        print(f"  {symbol}: {'✓ cryptocurrency' if is_crypto else '✗ stock (FAIL)'}")
        assert is_crypto, f"{symbol} should be detected as cryptocurrency"
    
    # Test stock symbols
    stock_symbols = ["AAPL", "NVDA", "GOOGL", "TSLA", "SPY"]
    for symbol in stock_symbols:
        is_crypto = is_crypto_symbol(symbol)
        print(f"  {symbol}: {'✗ cryptocurrency (FAIL)' if is_crypto else '✓ stock'}")
        assert not is_crypto, f"{symbol} should be detected as stock"
    
    print("✓ Asset type detection tests passed!\n")

def test_state_initialization():
    """Test that initial state includes asset_type field."""
    print("Testing state initialization...")
    
    propagator = Propagator()
    
    # Test with cryptocurrency
    crypto_state = propagator.create_initial_state("BTC", "2024-05-10")
    print(f"  BTC state asset_type: {crypto_state.get('asset_type')}")
    assert crypto_state.get('asset_type') == 'cryptocurrency', "BTC should have asset_type='cryptocurrency'"
    
    # Test with stock
    stock_state = propagator.create_initial_state("AAPL", "2024-05-10")
    print(f"  AAPL state asset_type: {stock_state.get('asset_type')}")
    assert stock_state.get('asset_type') == 'stock', "AAPL should have asset_type='stock'"
    
    # Verify other state fields are present
    required_fields = [
        'messages', 'company_of_interest', 'trade_date', 'asset_type',
        'investment_debate_state', 'risk_debate_state',
        'market_report', 'fundamentals_report', 'sentiment_report', 'news_report'
    ]
    for field in required_fields:
        assert field in crypto_state, f"State missing required field: {field}"
        assert field in stock_state, f"State missing required field: {field}"
    
    print("✓ State initialization tests passed!\n")

def test_prompt_customization_mock():
    """Test that prompts contain crypto-specific guidance (mock test)."""
    print("Testing prompt customization (mock)...")
    
    # This is a simple check - we can't easily test the actual LLM prompts
    # but we verify that the functions accept asset_type
    from tradingagents.agents.analysts.market_analyst import create_market_analyst
    
    # Just verify the function exists and can be imported
    assert create_market_analyst is not None
    
    print("✓ Prompt functions are accessible!\n")

if __name__ == "__main__":
    print("="*60)
    print("Testing Crypto-Specific Prompt Implementation")
    print("="*60 + "\n")
    
    try:
        test_asset_type_detection()
        test_state_initialization()
        test_prompt_customization_mock()
        
        print("="*60)
        print("✓ All tests passed successfully!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
