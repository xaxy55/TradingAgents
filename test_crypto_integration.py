"""
Integration test for cryptocurrency support in TradingAgents.

This test validates that the get_stock_data tool correctly routes
cryptocurrency symbols to crypto data providers.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_stock_data_tool_routing():
    """Test that get_stock_data tool correctly routes to crypto or stock data."""
    print("\n=== Testing get_stock_data Tool Routing ===")
    
    from tradingagents.agents.utils.core_stock_tools import get_stock_data
    from unittest.mock import patch
    
    # Mock the route_to_vendor function to verify correct routing
    with patch('tradingagents.agents.utils.core_stock_tools.route_to_vendor') as mock_route:
        mock_route.return_value = "Mocked data"
        
        # Test with a cryptocurrency symbol
        print("\nTesting with BTC (cryptocurrency)...")
        get_stock_data.invoke({
            "symbol": "BTC",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31"
        })
        
        # Verify it was routed to crypto endpoint
        assert mock_route.called, "route_to_vendor should have been called"
        call_args = mock_route.call_args[0]
        assert call_args[0] == "get_crypto_price", f"Expected get_crypto_price, got {call_args[0]}"
        assert call_args[1] == "BTC", f"Expected BTC symbol, got {call_args[1]}"
        print(f"✓ BTC correctly routed to: {call_args[0]}")
        print(f"  Arguments: symbol={call_args[1]}, market={call_args[2]}, start={call_args[3]}, end={call_args[4]}")
        
        # Reset mock
        mock_route.reset_mock()
        
        # Test with a stock symbol
        print("\nTesting with AAPL (stock)...")
        get_stock_data.invoke({
            "symbol": "AAPL",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31"
        })
        
        # Verify it was routed to stock endpoint
        assert mock_route.called, "route_to_vendor should have been called"
        call_args = mock_route.call_args[0]
        assert call_args[0] == "get_stock_data", f"Expected get_stock_data, got {call_args[0]}"
        assert call_args[1] == "AAPL", f"Expected AAPL symbol, got {call_args[1]}"
        print(f"✓ AAPL correctly routed to: {call_args[0]}")
        print(f"  Arguments: symbol={call_args[1]}, start={call_args[2]}, end={call_args[3]}")
    
    print("\n✓ All routing tests passed!\n")


def test_crypto_tools_available():
    """Test that crypto tools can be imported and invoked."""
    print("\n=== Testing Crypto Tools Availability ===")
    
    from tradingagents.agents.utils.crypto_tools import (
        get_crypto_price,
        get_crypto_intraday,
        detect_asset_type
    )
    
    # Test that tools are properly decorated
    assert hasattr(get_crypto_price, 'invoke'), "get_crypto_price should be a LangChain tool"
    assert hasattr(get_crypto_intraday, 'invoke'), "get_crypto_intraday should be a LangChain tool"
    assert hasattr(detect_asset_type, 'invoke'), "detect_asset_type should be a LangChain tool"
    
    print("✓ get_crypto_price tool available")
    print("✓ get_crypto_intraday tool available")
    print("✓ detect_asset_type tool available")
    
    print("\n✓ All crypto tools are available!\n")


def test_interface_complete():
    """Test that the interface module has all necessary components."""
    print("\n=== Testing Interface Completeness ===")
    
    from tradingagents.dataflows import interface
    
    # Check imports
    assert hasattr(interface, 'get_crypto_price_alpha_vantage'), "get_crypto_price_alpha_vantage should be imported"
    assert hasattr(interface, 'get_crypto_intraday_alpha_vantage'), "get_crypto_intraday_alpha_vantage should be imported"
    print("✓ Crypto dataflow functions imported")
    
    # Check TOOLS_CATEGORIES
    assert "cryptocurrency_data" in interface.TOOLS_CATEGORIES, "cryptocurrency_data category should exist"
    crypto_category = interface.TOOLS_CATEGORIES["cryptocurrency_data"]
    assert "get_crypto_price" in crypto_category["tools"], "get_crypto_price should be in crypto tools"
    assert "get_crypto_intraday" in crypto_category["tools"], "get_crypto_intraday should be in crypto tools"
    print(f"✓ Crypto tools category configured: {crypto_category['tools']}")
    
    # Check VENDOR_METHODS
    assert "get_crypto_price" in interface.VENDOR_METHODS, "get_crypto_price vendor methods should exist"
    assert "get_crypto_intraday" in interface.VENDOR_METHODS, "get_crypto_intraday vendor methods should exist"
    assert "alpha_vantage" in interface.VENDOR_METHODS["get_crypto_price"], "alpha_vantage vendor for crypto should exist"
    print("✓ Vendor methods configured for crypto")
    
    print("\n✓ Interface is complete!\n")


def main():
    """Run all integration tests."""
    print("\n" + "="*60)
    print("TradingAgents Cryptocurrency Integration Tests")
    print("="*60)
    
    try:
        test_stock_data_tool_routing()
        test_crypto_tools_available()
        test_interface_complete()
        
        print("\n" + "="*60)
        print("✓ ALL INTEGRATION TESTS PASSED!")
        print("="*60)
        print("\nCryptocurrency support is fully integrated!")
        print("You can now use TradingAgents with crypto symbols like BTC, ETH, etc.")
        print("\n")
        
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
