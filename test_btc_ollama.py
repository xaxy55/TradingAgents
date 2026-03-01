"""
Test: BTC Trading Agent with Ollama

This test validates that the TradingAgents framework works correctly
with Bitcoin (BTC) cryptocurrency and Ollama as the LLM provider.
"""

import sys
import os

# Add parent directory to path to import tradingagents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import copy
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def check_ollama_connection():
    """Check if Ollama server is accessible."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def test_ollama_configuration():
    """Test that Ollama is properly configured in the codebase."""
    print("\n=== Testing Ollama Configuration ===")
    
    # Check that Ollama is in the CLI utils
    from cli.utils import PROVIDER_URLS
    assert "ollama" in PROVIDER_URLS, "Ollama should be in PROVIDER_URLS"
    assert PROVIDER_URLS["ollama"] == "http://localhost:11434/v1", "Ollama URL should be correct"
    print("✓ Ollama provider configured in CLI utils")
    
    # Check that Ollama models are available in CLI
    from cli.utils import select_deep_thinking_agent, select_shallow_thinking_agent
    import inspect
    
    # Check the source code contains ollama options
    deep_source = inspect.getsource(select_deep_thinking_agent)
    shallow_source = inspect.getsource(select_shallow_thinking_agent)
    
    assert "ollama" in deep_source.lower(), "Ollama should be in deep thinking agent options"
    assert "ollama" in shallow_source.lower(), "Ollama should be in shallow thinking agent options"
    print("✓ Ollama models available in CLI selections")
    
    print("\n✓ Ollama configuration tests passed!\n")


def test_btc_symbol_detection():
    """Test that BTC is correctly identified as a cryptocurrency."""
    print("\n=== Testing BTC Symbol Detection ===")
    
    from tradingagents.dataflows.crypto_dataflows import is_crypto_symbol
    
    result = is_crypto_symbol("BTC")
    assert result, "BTC should be detected as cryptocurrency"
    print("✓ BTC correctly detected as cryptocurrency")
    
    from tradingagents.agents.utils.crypto_tools import detect_asset_type
    asset_type = detect_asset_type.invoke({"symbol": "BTC"})
    assert asset_type == "cryptocurrency", "BTC should be detected as cryptocurrency by tool"
    print("✓ BTC asset type detection working")
    
    print("\n✓ BTC symbol detection tests passed!\n")


def test_ollama_trading_graph_initialization():
    """Test that TradingAgentsGraph can be initialized with Ollama config."""
    print("\n=== Testing TradingAgentsGraph Initialization with Ollama ===")
    
    # Create Ollama configuration
    config = copy.deepcopy(DEFAULT_CONFIG)
    config["llm_provider"] = "ollama"
    config["backend_url"] = "http://localhost:11434/v1"
    config["deep_think_llm"] = "llama3.1"
    config["quick_think_llm"] = "llama3.1"
    config["crypto_settings"]["default_market"] = "USD"
    
    print(f"Config LLM provider: {config['llm_provider']}")
    print(f"Config backend URL: {config['backend_url']}")
    print(f"Config deep model: {config['deep_think_llm']}")
    print(f"Config quick model: {config['quick_think_llm']}")
    
    try:
        # This should not raise an error even if Ollama is not running
        # We're just testing the configuration and initialization
        ta = TradingAgentsGraph(debug=False, config=config)
        print("✓ TradingAgentsGraph initialized with Ollama config")
        
        # Check that the correct LLM type is used
        from langchain_openai import ChatOpenAI
        assert isinstance(ta.deep_thinking_llm, ChatOpenAI), "Should use ChatOpenAI for Ollama"
        assert isinstance(ta.quick_thinking_llm, ChatOpenAI), "Should use ChatOpenAI for Ollama"
        print("✓ Correct LLM classes instantiated (ChatOpenAI for Ollama)")
        
    except Exception as e:
        print(f"✗ Error initializing TradingAgentsGraph: {e}")
        raise
    
    print("\n✓ TradingAgentsGraph initialization tests passed!\n")


def test_full_btc_analysis_with_ollama():
    """
    Test full BTC analysis with Ollama (only if Ollama is running).
    This is an integration test that requires:
    - Ollama running locally
    - At least one model pulled (e.g., llama3.1)
    - ALPHA_VANTAGE_API_KEY set
    """
    print("\n=== Testing Full BTC Analysis with Ollama ===")
    
    # Check prerequisites
    if not check_ollama_connection():
        print("⚠️  Skipping full analysis test: Ollama server not available")
        print("   To run this test:")
        print("   1. Install Ollama from https://ollama.ai")
        print("   2. Run: ollama pull llama3.1")
        print("   3. Ensure Ollama server is running")
        return
    
    if not os.getenv("ALPHA_VANTAGE_API_KEY"):
        print("⚠️  Skipping full analysis test: ALPHA_VANTAGE_API_KEY not set")
        print("   Set your API key: export ALPHA_VANTAGE_API_KEY=your_key_here")
        return
    
    print("✓ Ollama server is running")
    print("✓ ALPHA_VANTAGE_API_KEY is set")
    print("\nRunning full BTC analysis (this may take several minutes)...")
    
    # Create configuration for Ollama
    config = copy.deepcopy(DEFAULT_CONFIG)
    config["llm_provider"] = "ollama"
    config["backend_url"] = "http://localhost:11434/v1"
    config["deep_think_llm"] = "llama3.1"
    config["quick_think_llm"] = "llama3.1"
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1
    config["crypto_settings"]["default_market"] = "USD"
    
    try:
        ta = TradingAgentsGraph(debug=True, config=config)
        _, decision = ta.propagate("BTC", "2024-05-10")
        
        print("\n✓ BTC analysis completed successfully with Ollama!")
        print(f"\nDecision summary: {str(decision)[:200]}...")
        
        # Basic validation of decision
        assert decision is not None, "Decision should not be None"
        print("✓ Valid decision returned")
        
    except Exception as e:
        print(f"\n✗ Error during BTC analysis: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    print("\n✓ Full BTC analysis test passed!\n")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("Testing TradingAgents: BTC with Ollama")
    print("="*70)
    
    try:
        # Core configuration tests (always run)
        test_ollama_configuration()
        test_btc_symbol_detection()
        test_ollama_trading_graph_initialization()
        
        # Integration test (only if prerequisites are met)
        test_full_btc_analysis_with_ollama()
        
        print("\n" + "="*70)
        print("✓ ALL TESTS PASSED!")
        print("="*70)
        print("\nSummary:")
        print("  • Ollama configuration: ✓ Working")
        print("  • BTC symbol detection: ✓ Working")
        print("  • TradingGraph initialization: ✓ Working")
        print("  • Full analysis: Check output above")
        print("\nYou can now use TradingAgents to analyze BTC with Ollama!")
        print("Run: python example_crypto_ollama.py")
        print("="*70 + "\n")
        
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
