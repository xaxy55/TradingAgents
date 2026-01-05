# Cryptocurrency Support in TradingAgents

TradingAgents now supports cryptocurrency trading analysis! This document explains how to use the framework to analyze Bitcoin, Ethereum, and other major cryptocurrencies.

## Overview

The cryptocurrency support is fully integrated into the existing TradingAgents framework. You can analyze crypto assets using the same multi-agent architecture that's used for stocks, with automatic detection and routing to appropriate data sources.

## Supported Cryptocurrencies

The framework currently supports 30+ major cryptocurrencies including:

- **Bitcoin (BTC)**
- **Ethereum (ETH)**
- **Stablecoins:** USDT, USDC
- **Major Altcoins:** BNB, SOL, XRP, ADA, DOGE, DOT, MATIC, LTC, AVAX, UNI, LINK, ATOM, and more

The system automatically detects cryptocurrency symbols and routes them to the appropriate data provider.

## Quick Start

### Using the CLI

```bash
python -m cli.main
```

When prompted for a ticker symbol, enter a cryptocurrency symbol like:
- `BTC` for Bitcoin
- `ETH` for Ethereum
- `SOL` for Solana

The framework will automatically detect that it's a cryptocurrency and use the appropriate data sources.

### Using Python API

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Configure for crypto analysis
config = DEFAULT_CONFIG.copy()
config["crypto_settings"]["default_market"] = "USD"
config["data_vendors"]["cryptocurrency_data"] = "alpha_vantage"

# Initialize
ta = TradingAgentsGraph(debug=True, config=config)

# Analyze Bitcoin
_, decision = ta.propagate("BTC", "2024-05-10")
print(decision)
```

## Configuration

### Crypto-Specific Settings

You can configure cryptocurrency-specific parameters in `default_config.py` or override them in your config:

```python
config["crypto_settings"] = {
    "default_market": "USD",      # Default fiat/stablecoin pair
    "default_interval": "60min",  # Default interval for intraday data
}
```

### Data Vendors

Configure which data provider to use for cryptocurrency data:

```python
config["data_vendors"]["cryptocurrency_data"] = "alpha_vantage"
```

Currently supported vendors:
- **alpha_vantage**: Uses Alpha Vantage's cryptocurrency endpoints (default)

## Available Tools

The framework provides several tools for cryptocurrency analysis:

### 1. `get_crypto_price`
Retrieve historical cryptocurrency price data (OHLCV).

```python
from tradingagents.agents.utils.crypto_tools import get_crypto_price

result = get_crypto_price.invoke({
    "symbol": "BTC",
    "market": "USD",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
})
```

### 2. `get_crypto_intraday`
Retrieve intraday cryptocurrency data for technical analysis.

```python
from tradingagents.agents.utils.crypto_tools import get_crypto_intraday

result = get_crypto_intraday.invoke({
    "symbol": "ETH",
    "market": "USD",
    "interval": "60min"  # Options: 1min, 5min, 15min, 30min, 60min
})
```

### 3. `detect_asset_type`
Automatically detect if a symbol is a cryptocurrency or stock.

```python
from tradingagents.agents.utils.crypto_tools import detect_asset_type

asset_type = detect_asset_type.invoke({"symbol": "BTC"})
# Returns: "cryptocurrency"

asset_type = detect_asset_type.invoke({"symbol": "AAPL"})
# Returns: "stock"
```

## Automatic Detection

The framework automatically detects cryptocurrency symbols in the `get_stock_data` tool, which has been enhanced to support both stocks and cryptocurrencies:

```python
from tradingagents.agents.utils.core_stock_tools import get_stock_data

# This automatically detects BTC is a crypto and routes to crypto provider
btc_data = get_stock_data.invoke({
    "symbol": "BTC",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
})

# This detects AAPL is a stock and routes to stock provider
aapl_data = get_stock_data.invoke({
    "symbol": "AAPL",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
})
```

## Multi-Agent Analysis for Crypto

When you analyze a cryptocurrency, all the standard TradingAgents teams work on it:

1. **Analyst Team**
   - Market Analyst: Technical analysis using price patterns and indicators
   - News Analyst: Sentiment analysis from crypto news sources
   - (Note: Fundamental analysis is limited for crypto compared to stocks)

2. **Research Team**
   - Bull Researcher: Identifies bullish signals and opportunities
   - Bear Researcher: Identifies bearish signals and risks
   - Research Manager: Synthesizes both perspectives

3. **Trading Team**
   - Trader: Proposes trading positions based on analysis

4. **Risk Management Team**
   - Evaluates portfolio risk and position sizing
   - Considers crypto-specific volatility factors

5. **Portfolio Manager**
   - Makes final trading decision

## Example: Complete Crypto Analysis

See `example_crypto.py` for a complete example:

```bash
python example_crypto.py
```

This demonstrates:
- Analyzing Bitcoin (BTC)
- Analyzing Ethereum (ETH)
- How the multi-agent system processes crypto assets
- Final trading decisions

## Data Sources

### Alpha Vantage (Default)

Alpha Vantage provides cryptocurrency data through their API:
- Daily OHLCV data: `DIGITAL_CURRENCY_DAILY`
- Intraday data: `CRYPTO_INTRADAY`
- News sentiment (covers crypto news)

Get a free API key: https://www.alphavantage.co/support/#api-key

### Future Data Sources

The modular architecture allows easy addition of other crypto data providers:
- CoinGecko API
- Binance API
- Coinbase API
- Custom data feeds

## Differences from Stock Analysis

When analyzing cryptocurrencies, be aware of these differences:

### Similarities
✓ Technical analysis (price patterns, indicators)
✓ News sentiment analysis
✓ Risk management framework
✓ Multi-agent debate and decision-making

### Differences
- ✗ No traditional fundamental data (P/E ratios, earnings, etc.)
- ⚠️ Higher volatility requires adjusted risk parameters
- 🕐 24/7 trading (no market hours)
- 🌍 Global, decentralized markets

## Troubleshooting

### "No data found for symbol"
- Verify the cryptocurrency symbol is correct (use uppercase: BTC, not btc)
- Check that the symbol is supported by your data provider
- Ensure your API key has cryptocurrency data access

### "Rate limit exceeded"
- Alpha Vantage has rate limits (usually 5 calls/min for free tier)
- Consider upgrading to Alpha Vantage Premium
- Use data caching to reduce API calls

### "Module not found" errors
- Install requirements: `pip install -r requirements.txt`
- Ensure all dependencies are installed

## Testing

Run the cryptocurrency test suite:

```bash
# Unit tests
python test_crypto.py

# Integration tests
python test_crypto_integration.py
```

## Contributing

To add support for additional cryptocurrencies or data sources:

1. Add the crypto symbol to `is_crypto_symbol()` in `crypto_dataflows.py`
2. Implement data fetching functions in `crypto_dataflows.py`
3. Add vendor mapping in `interface.py`
4. Update tests

## API Reference

### Crypto Dataflows Module
- `get_crypto_price_alpha_vantage()`: Fetch crypto price data
- `get_crypto_intraday_alpha_vantage()`: Fetch intraday crypto data
- `is_crypto_symbol()`: Detect crypto symbols

### Crypto Tools Module
- `get_crypto_price`: LangChain tool for crypto prices
- `get_crypto_intraday`: LangChain tool for intraday data
- `detect_asset_type`: LangChain tool for asset type detection

## Future Enhancements

Planned features:
- [ ] On-chain metrics (transaction volume, active addresses)
- [ ] DeFi protocol analysis
- [ ] Cross-chain analysis
- [ ] Crypto-specific risk metrics (volatility, liquidity)
- [ ] Integration with more exchanges (Binance, Coinbase, etc.)
- [ ] NFT market analysis

## Support

For questions or issues:
- Check the main README.md
- Open an issue on GitHub
- Join the Discord community

## License

Same as TradingAgents main project (see LICENSE file).
