# AI Agent Instructions for TradingAgents

This file provides vendor-neutral instructions for AI coding agents working with the TradingAgents repository.

## Project Summary

**TradingAgents** is a multi-agent LLM-powered trading framework that mirrors real-world trading firms. It uses specialized AI agents (analysts, researchers, traders, risk managers) to collaboratively evaluate market conditions and make trading decisions for both stocks and cryptocurrencies.

**Technology Stack**: Python 3.10+, LangGraph, LangChain, yfinance, Alpha Vantage API, OpenAI/Gemini/Claude

## Repository Structure

```
TradingAgents/
├── .github/                      # GitHub configuration and Copilot instructions
├── tradingagents/               # Main package
│   ├── agents/                  # Agent implementations
│   │   ├── analysts/           # Fundamental, sentiment, news, technical analysts
│   │   ├── researchers/        # Bull and bear researchers
│   │   ├── managers/           # Risk and portfolio managers
│   │   ├── traders/            # Trading decision agents
│   │   └── utils/              # Agent utilities and tools
│   ├── dataflows/              # Data fetching and processing
│   │   └── data_cache/         # Cached data
│   └── graph/                  # LangGraph workflow orchestration
├── cli/                         # Command-line interface
├── assets/                      # Images and media
├── test_*.py                    # Test files
├── example_*.py                 # Usage examples
└── main.py                      # Main entry point
```

## Development Setup

### Prerequisites

- Python 3.10 or higher
- pip package manager
- API keys: OpenAI, Alpha Vantage (Google/Anthropic optional)

### Installation

```bash
# Clone repository
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents

# Create virtual environment
conda create -n tradingagents python=3.13
conda activate tradingagents

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

### Running the Application

```bash
# Interactive CLI
python -m cli.main

# Python API
python main.py

# Cryptocurrency examples
python example_crypto.py
python example_crypto_gemini.py

# Run tests
python test_crypto.py
python -m pytest
```

## Coding Conventions

### Python Style Guide

- **Formatting**: Follow PEP 8 with 88-100 character line length
- **Type Hints**: Always use type hints for function signatures
- **Docstrings**: Document all public APIs with clear, concise docstrings
- **Variable Naming**: 
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`

### Example Code Pattern

```python
from typing import Optional, Dict, Any
from tradingagents.default_config import DEFAULT_CONFIG

def fetch_market_data(
    ticker: str,
    date: str,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fetch market data for a given ticker and date.
    
    Args:
        ticker: Stock or crypto symbol (e.g., "AAPL", "BTC")
        date: Date in YYYY-MM-DD format
        config: Optional configuration dictionary
        
    Returns:
        Dictionary containing market data
        
    Raises:
        ValueError: If ticker or date format is invalid
    """
    if config is None:
        config = DEFAULT_CONFIG.copy()
    
    # Implementation
    pass
```

## Architecture Patterns

### Agent Implementation

All agents follow a consistent structure:

1. **State Management**: Use `tradingagents/agents/utils/agent_states.py`
2. **LLM Integration**: Access via config (`deep_think_llm`, `quick_think_llm`)
3. **Data Tools**: Import from `tradingagents/agents/utils/*_tools.py`
4. **Graph Nodes**: Implement as LangGraph nodes in `tradingagents/graph/`

### Configuration Management

```python
import copy
from tradingagents.default_config import DEFAULT_CONFIG

# Always copy the config before modifying
config = copy.deepcopy(DEFAULT_CONFIG)
config["llm_provider"] = "google"
config["deep_think_llm"] = "gemini-2.0-flash"
config["max_debate_rounds"] = 2
```

### Data Vendor Pattern

The framework supports multiple data vendors. When adding new data sources:

1. Add vendor to `data_vendors` or `tool_vendors` in config
2. Implement data fetching in `tradingagents/dataflows/`
3. Follow existing patterns (e.g., `y_finance.py`, `alpha_vantage.py`)
4. Handle rate limits and caching appropriately

## Testing Guidelines

### Test File Conventions

- Place tests at repository root with `test_` prefix
- Name tests descriptively: `test_[feature]_[scenario].py`
- Use pytest for test discovery and execution

### Test Structure

```python
def test_crypto_data_fetching():
    """Test that cryptocurrency data can be fetched successfully."""
    # Arrange
    ticker = "BTC"
    date = "2024-05-10"
    
    # Act
    result = fetch_crypto_data(ticker, date)
    
    # Assert
    assert result is not None
    assert "price" in result
```

### Mocking External APIs

Always mock external API calls in tests to:
- Avoid rate limits
- Ensure test reliability
- Speed up test execution

## Multi-Asset Support

### Stock Trading

- Use standard ticker symbols: "AAPL", "NVDA", "TSLA"
- Data sources: yfinance, Alpha Vantage
- Supports fundamental analysis, earnings, balance sheets

### Cryptocurrency Trading

- Use crypto symbols: "BTC", "ETH", "SOL"
- Data sources: Alpha Vantage cryptocurrency APIs
- Limited fundamental data, focus on technical and sentiment analysis
- Configure with: `config["crypto_settings"]["default_market"] = "USD"`

The framework automatically detects asset type and uses appropriate data sources.

## LLM Provider Configuration

### Supported Providers

- **OpenAI**: gpt-4o, gpt-4o-mini, o1-preview, o1-mini
- **Google**: gemini-2.0-flash, gemini-2.0-flash-lite
- **Anthropic**: claude-3-opus, claude-3-sonnet

### Switching Providers

```python
# OpenAI (default)
config["llm_provider"] = "openai"
config["deep_think_llm"] = "gpt-4o"
config["quick_think_llm"] = "gpt-4o-mini"

# Google Gemini
config["llm_provider"] = "google"
config["backend_url"] = "https://generativelanguage.googleapis.com/v1"
config["deep_think_llm"] = "gemini-2.0-flash"
config["quick_think_llm"] = "gemini-2.0-flash-lite"

# Anthropic Claude
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-3-opus-20240229"
```

## Common Tasks

### Adding a New Agent

1. Create agent file in appropriate `tradingagents/agents/[category]/` directory
2. Inherit from base agent class or follow existing agent pattern
3. Implement required methods and LangGraph node function
4. Register agent in `tradingagents/graph/trading_graph.py`
5. Add corresponding tests

### Adding a New Data Source

1. Create module in `tradingagents/dataflows/`
2. Implement data fetching functions following existing patterns
3. Add vendor configuration to `default_config.py`
4. Update relevant tool files in `tradingagents/agents/utils/`
5. Add tests with mocked API responses

### Extending Cryptocurrency Support

1. Check if feature applies to crypto (some features are stock-specific)
2. Implement crypto-specific logic in `tradingagents/agents/utils/crypto_tools.py`
3. Update config with crypto settings if needed
4. Test with BTC, ETH examples

## Performance Considerations

- **API Costs**: Framework makes many LLM API calls; use smaller models for testing
- **Rate Limits**: 
  - Alpha Vantage: 60 requests/minute for TradingAgents users
  - OpenAI: Based on tier
  - yfinance: No official rate limit but be respectful
- **Caching**: Use data cache directory to avoid redundant API calls
- **Async Operations**: Consider async patterns for parallel data fetching

## Environment Variables

Required:
```bash
OPENAI_API_KEY=sk-...                    # For OpenAI models
ALPHA_VANTAGE_API_KEY=YOUR_KEY           # For market data
```

Optional:
```bash
GOOGLE_API_KEY=...                       # For Gemini models
ANTHROPIC_API_KEY=...                    # For Claude models
TRADINGAGENTS_RESULTS_DIR=./results      # Custom results directory
```

## Best Practices

1. **Always copy config**: Use `copy.deepcopy(DEFAULT_CONFIG)` before modifying
2. **Type hints everywhere**: Help IDEs and other developers understand your code
3. **Document public APIs**: Clear docstrings for all exported functions
4. **Test with multiple providers**: Ensure code works with OpenAI, Gemini, Claude
5. **Handle errors gracefully**: Trading systems should be resilient
6. **Mock external calls**: Don't hit real APIs in tests
7. **Consider costs**: Be mindful of LLM API usage
8. **Version compatibility**: Target Python 3.10+ for modern features

## Resources

- **arXiv Paper**: https://arxiv.org/abs/2412.20138
- **Documentation**: See README.md and implementation guides
- **Community**: Discord, GitHub Discussions
- **Alpha Vantage API**: https://www.alphavantage.co/support/#api-key

## Disclaimer

TradingAgents is designed for research purposes. Trading performance varies based on many factors including model choice, temperature, trading periods, and data quality. **This is not financial, investment, or trading advice.**
