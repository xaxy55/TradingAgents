"""
Test cryptocurrency data providers and tools.

This test file validates the cryptocurrency monitoring functionality
added to TradingAgents.
"""

import sys
import os

# Add parent directory to path to import tradingagents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tradingagents.dataflows.crypto_dataflows import (
    is_crypto_symbol,
)


def test_crypto_symbol_detection():
    """Test that we can correctly identify cryptocurrency symbols."""
    print("\n=== Testing Crypto Symbol Detection ===")
    
    # Test known cryptocurrencies
    crypto_symbols = ['BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'DOGE']
    for symbol in crypto_symbols:
        result = is_crypto_symbol(symbol)
        print(f"{symbol}: {'✓ Detected as crypto' if result else '✗ NOT detected as crypto'}")
        assert result, f"{symbol} should be detected as crypto"
    
    # Test known stocks
    stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'SPY']
    for symbol in stock_symbols:
        result = is_crypto_symbol(symbol)
        print(f"{symbol}: {'✗ Detected as crypto (WRONG!)' if result else '✓ Correctly identified as stock'}")
        assert not result, f"{symbol} should NOT be detected as crypto"
    
    print("\n✓ All crypto symbol detection tests passed!\n")


def test_ambiguous_symbol_detection():
    """Test detection of symbols that could be both crypto and stock."""
    print("\n=== Testing Ambiguous Symbol Detection ===")
    
    # Test ambiguous symbols - these should NOT be detected as crypto
    # to avoid misrouting stock data
    ambiguous_symbols = ['CRO', 'ICP', 'VET', 'NEAR']
    for symbol in ambiguous_symbols:
        result = is_crypto_symbol(symbol)
        print(f"{symbol}: {'✗ Detected as crypto (ambiguous symbol)' if result else '✓ Not detected as crypto (avoiding collision)'}")
        assert not result, f"{symbol} is ambiguous and should NOT be auto-detected as crypto to avoid stock ticker collision"
    
    print("\n✓ All ambiguous symbol detection tests passed!\n")


def test_detect_asset_type_tool():
    """Test the LangChain tool for asset type detection."""
    print("\n=== Testing Asset Type Detection Tool ===")
    
    # Import the tool
    from tradingagents.agents.utils.crypto_tools import detect_asset_type
    
    # Test with cryptocurrencies
    result = detect_asset_type.invoke({"symbol": "BTC"})
    print(f"BTC detected as: {result}")
    assert result == "cryptocurrency", "BTC should be detected as cryptocurrency"
    
    result = detect_asset_type.invoke({"symbol": "ETH"})
    print(f"ETH detected as: {result}")
    assert result == "cryptocurrency", "ETH should be detected as cryptocurrency"
    
    # Test with stocks
    result = detect_asset_type.invoke({"symbol": "AAPL"})
    print(f"AAPL detected as: {result}")
    assert result == "stock", "AAPL should be detected as stock"
    
    print("\n✓ All asset type detection tool tests passed!\n")


def test_crypto_data_routing():
    """Test that crypto data routing is properly configured."""
    print("\n=== Testing Crypto Data Routing ===")
    
    from tradingagents.dataflows.interface import (
        TOOLS_CATEGORIES,
        VENDOR_METHODS,
        get_category_for_method,
    )
    
    # Check that cryptocurrency_data category exists
    assert "cryptocurrency_data" in TOOLS_CATEGORIES, "cryptocurrency_data category should exist"
    print("✓ cryptocurrency_data category exists")
    
    # Check that crypto tools are registered
    crypto_tools = TOOLS_CATEGORIES["cryptocurrency_data"]["tools"]
    assert "get_crypto_price" in crypto_tools, "get_crypto_price should be in crypto tools"
    assert "get_crypto_intraday" in crypto_tools, "get_crypto_intraday should be in crypto tools"
    print(f"✓ Crypto tools registered: {crypto_tools}")
    
    # Check that vendor methods are configured
    assert "get_crypto_price" in VENDOR_METHODS, "get_crypto_price should have vendor methods"
    assert "get_crypto_intraday" in VENDOR_METHODS, "get_crypto_intraday should have vendor methods"
    print("✓ Vendor methods configured for crypto tools")
    
    # Check category lookup
    category = get_category_for_method("get_crypto_price")
    assert category == "cryptocurrency_data", "get_crypto_price should be in cryptocurrency_data category"
    print(f"✓ get_crypto_price correctly mapped to {category} category")
    
    print("\n✓ All crypto data routing tests passed!\n")


def test_config_has_crypto_settings():
    """Test that default config includes crypto settings."""
    print("\n=== Testing Configuration ===")
    
    from tradingagents.default_config import DEFAULT_CONFIG
    
    # Check that crypto_settings exists
    assert "crypto_settings" in DEFAULT_CONFIG, "crypto_settings should exist in DEFAULT_CONFIG"
    print("✓ crypto_settings exists in config")
    
    # Check crypto_settings content
    crypto_settings = DEFAULT_CONFIG["crypto_settings"]
    assert "default_market" in crypto_settings, "default_market should be in crypto_settings"
    assert "default_interval" in crypto_settings, "default_interval should be in crypto_settings"
    print(f"✓ Crypto settings configured: {crypto_settings}")
    
    # Check that cryptocurrency_data vendor is configured
    assert "cryptocurrency_data" in DEFAULT_CONFIG["data_vendors"], "cryptocurrency_data should be in data_vendors"
    print(f"✓ Cryptocurrency data vendor: {DEFAULT_CONFIG['data_vendors']['cryptocurrency_data']}")
    
    print("\n✓ All configuration tests passed!\n")


def test_interval_validation():
    """Test validation of interval parameters."""
    print("\n=== Testing Interval Validation ===")
    
    from tradingagents.dataflows.crypto_dataflows import get_crypto_intraday_alpha_vantage
    
    # Test valid intervals - we'll just check the function doesn't error on validation
    valid_intervals = ["1min", "5min", "15min", "30min", "60min"]
    print(f"Valid intervals: {', '.join(valid_intervals)}")
    
    # Test invalid interval
    result = get_crypto_intraday_alpha_vantage("BTC", "USD", "2min")
    assert "Error: Invalid interval" in result, "Should return error for invalid interval"
    print("✓ Invalid interval '2min' properly rejected")
    
    result = get_crypto_intraday_alpha_vantage("BTC", "USD", "invalid")
    assert "Error: Invalid interval" in result, "Should return error for invalid interval"
    print("✓ Invalid interval 'invalid' properly rejected")
    
    print("\n✓ All interval validation tests passed!\n")


def test_crypto_price_data_structure():
    """Test the structure of crypto price data (without API call)."""
    print("\n=== Testing Crypto Price Data Structure ===")
    
    # We'll test the function signature and error handling without making actual API calls
    from tradingagents.dataflows.crypto_dataflows import get_crypto_price_alpha_vantage
    import inspect
    
    # Check function signature
    sig = inspect.signature(get_crypto_price_alpha_vantage)
    params = list(sig.parameters.keys())
    assert "symbol" in params, "symbol parameter should exist"
    assert "market" in params, "market parameter should exist"
    print(f"✓ Function signature correct: {params}")
    
    print("\n✓ Crypto price data structure test passed!\n")
    print("Note: Actual API calls are not tested to avoid rate limits and API key requirements.")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Testing TradingAgents Cryptocurrency Support")
    print("="*60)
    
    try:
        test_crypto_symbol_detection()
        test_ambiguous_symbol_detection()
        test_detect_asset_type_tool()
        test_crypto_data_routing()
        test_config_has_crypto_settings()
        test_interval_validation()
        test_crypto_price_data_structure()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60 + "\n")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
