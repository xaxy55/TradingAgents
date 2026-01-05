# GitHub Copilot Instructions for TradingAgents

## Project Overview

TradingAgents is a multi-agent trading framework powered by Large Language Models (LLMs). The system deploys specialized AI agents (fundamental analysts, sentiment experts, technical analysts, traders, and risk managers) that collaborate to evaluate market conditions and inform trading decisions.

## Architecture

The framework uses **LangGraph** for agent orchestration and supports multiple LLM providers (OpenAI, Google Gemini, Anthropic Claude).

### Key Components

- `tradingagents/agents/`: Individual agent implementations (analysts, researchers, traders, managers)
- `tradingagents/graph/`: LangGraph workflow orchestration
- `tradingagents/dataflows/`: Data fetching and processing (yfinance, Alpha Vantage, etc.)
- `cli/`: Command-line interface for user interaction
- Tests: `test_*.py` files at repository root

## Python Coding Standards

### General Rules

- **Python Version**: Target Python 3.10+
- **Type Hints**: Use type hints for all function parameters and return values
- **Docstrings**: Write docstrings for all public functions, classes, and methods
- **Naming Conventions**:
  - `snake_case` for functions, variables, and module names
  - `PascalCase` for class names
  - `UPPER_CASE` for constants
- **Line Length**: Aim for 88-100 characters per line (Black formatter style)
- **Imports**: Group imports in order: standard library, third-party packages, local modules

### Code Style

```python
# Good example
def get_stock_data(ticker: str, start_date: str) -> dict:
    """
    Fetch stock data for the given ticker and date.
    
    Args:
        ticker: Stock symbol (e.g., "AAPL")
        start_date: Start date in YYYY-MM-DD format
        
    Returns:
        Dictionary containing stock data
    """
    pass
```

## LLM Integration Patterns

### Configuration

- LLM settings are defined in `tradingagents/default_config.py`
- Support multiple providers via `llm_provider` config key
- Use `deep_think_llm` for complex reasoning tasks
- Use `quick_think_llm` for faster, simpler tasks

### Agent Creation

- All agents should inherit from appropriate base classes in `tradingagents/agents/`
- Use LangGraph nodes for agent implementation
- Follow the existing agent structure for consistency

## Data Vendors

The framework supports multiple data vendors configurable in `default_config.py`:

- **core_stock_apis**: yfinance, alpha_vantage, local
- **technical_indicators**: yfinance, alpha_vantage, local
- **fundamental_data**: openai, alpha_vantage, local
- **news_data**: openai, alpha_vantage, google, local
- **cryptocurrency_data**: alpha_vantage

When adding new data sources, follow the existing pattern in `tradingagents/dataflows/`.

## Testing Practices

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python test_crypto.py

# Run with verbose output
python -m pytest -v
```

### Writing Tests

- Place test files at repository root with `test_` prefix
- Use descriptive test function names
- Test both stock and cryptocurrency functionality where applicable
- Mock external API calls to avoid rate limits

### Test Structure

```python
def test_feature_name():
    """Test description of what this test validates."""
    # Arrange
    config = DEFAULT_CONFIG.copy()
    
    # Act
    result = function_to_test(param)
    
    # Assert
    assert result is not None
```

## Development Commands

### Environment Setup

```bash
# Create virtual environment
conda create -n tradingagents python=3.13
conda activate tradingagents

# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .env.example .env
# Edit .env with your actual API keys
```

### Running the Application

```bash
# CLI interface
python -m cli.main

# Python API
python main.py

# Crypto examples
python example_crypto.py
python example_crypto_gemini.py
```

## Cryptocurrency vs Stock Trading

The framework automatically detects asset type based on ticker symbol:

- **Stocks**: Use traditional ticker symbols (e.g., "AAPL", "NVDA")
- **Cryptocurrencies**: Use crypto symbols (e.g., "BTC", "ETH")

When implementing new features:
- Check if feature applies to both asset types
- Use appropriate data sources (crypto uses different APIs)
- Test with both stock and crypto examples

## API Requirements

### Required APIs

- **OpenAI API**: For LLM agents (or alternative: Google Gemini, Anthropic Claude)
- **Alpha Vantage API**: For fundamental and news data (free tier available)

### Environment Variables

```bash
export OPENAI_API_KEY=$YOUR_OPENAI_API_KEY
export ALPHA_VANTAGE_API_KEY=$YOUR_ALPHA_VANTAGE_API_KEY
export GOOGLE_API_KEY=$YOUR_GOOGLE_API_KEY  # Optional, for Gemini
```

## Important Notes

- **Research Framework**: This is designed for research purposes, not financial advice
- **Rate Limits**: Be mindful of API rate limits when making data requests
- **Async Operations**: Framework makes multiple API calls; consider performance implications
- **Non-Deterministic**: Results may vary due to LLM temperature and other factors
- **Cost Management**: Use smaller models (e.g., gpt-4o-mini) for testing to reduce API costs

## File Organization

When adding new features:

- **New agents**: Add to `tradingagents/agents/[category]/`
- **New data sources**: Add to `tradingagents/dataflows/`
- **New tools**: Add to `tradingagents/agents/utils/`
- **Tests**: Add to repository root with `test_` prefix
- **Documentation**: Update README.md and relevant .md files

## Common Patterns

### Error Handling

```python
try:
    result = external_api_call()
except Exception as e:
    logger.error(f"API call failed: {e}")
    return default_value
```

### Configuration Access

```python
from tradingagents.default_config import DEFAULT_CONFIG
import copy

config = copy.deepcopy(DEFAULT_CONFIG)
config["llm_provider"] = "google"
```

### Agent Graph Usage

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("AAPL", "2024-05-10")
```
