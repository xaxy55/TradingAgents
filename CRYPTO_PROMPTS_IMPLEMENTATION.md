# Crypto-Specific Prompts Implementation

## Overview
This document describes the implementation of cryptocurrency-specific prompts in TradingAgents, which allows the system to provide tailored analysis for crypto assets vs traditional stocks.

## What Changed

### 1. Asset Type Detection
- **File**: `tradingagents/graph/propagation.py`
- **Change**: The `create_initial_state()` function now automatically detects if a ticker is a cryptocurrency or stock using `is_crypto_symbol()` and adds an `asset_type` field to the state.
- **Result**: Every agent in the pipeline now knows whether they're analyzing a crypto or stock.

### 2. Crypto-Aware Agent Prompts
All agents now check the `asset_type` field and adjust their prompts accordingly:

#### Market Analyst (`tradingagents/agents/analysts/market_analyst.py`)
- **Stock Mode**: Standard technical analysis guidance
- **Crypto Mode**: Additional considerations:
  - 24/7 trading patterns across time zones
  - Higher volatility expectations
  - Sentiment-driven price movements
  - Shorter timeframe indicators relevance
  - RSI and momentum in extreme zones longer

#### News Analyst (`tradingagents/agents/analysts/news_analyst.py`)
- **Stock Mode**: Standard news analysis
- **Crypto Mode**: Focus on:
  - Regulatory developments (SEC, government announcements)
  - Adoption news (institutional investment, ETF approvals)
  - Technical developments (network upgrades, protocol changes)
  - Security events (exchange hacks, vulnerabilities)
  - Influential figures' statements

#### Fundamentals Analyst (`tradingagents/agents/analysts/fundamentals_analyst.py`)
- **Stock Mode**: Traditional fundamental analysis (earnings, balance sheets, etc.)
- **Crypto Mode**: Adapted approach:
  - Acknowledges lack of traditional fundamentals
  - Focus on tokenomics, technology, team, and adoption
  - Explains why financial statement tools aren't applicable

#### Social Media Analyst (`tradingagents/agents/analysts/social_media_analyst.py`)
- **Stock Mode**: Standard social sentiment analysis
- **Crypto Mode**: Crypto-specific sources:
  - Twitter/X as major crypto news source
  - Reddit crypto communities
  - Influencer impact considerations
  - FUD and FOMO dynamics
  - Coordinated pump/dump awareness

#### Trader (`tradingagents/agents/trader/trader.py`)
- **Stock Mode**: Standard trading considerations
- **Crypto Mode**: Additional factors:
  - 24/7 market dynamics
  - High volatility adjustments
  - No circuit breakers
  - Liquidity concerns
  - Regulatory risk
  - Technical analysis prioritization

#### Research Team (Bull & Bear)
- **Bull Researcher**: Crypto-specific opportunities (adoption, innovation, institutional interest)
- **Bear Researcher**: Crypto-specific risks (regulatory, volatility, security, manipulation)

#### Risk Management Team
- **Aggressive Analyst**: Emphasizes exponential return potential, early adoption rewards
- **Conservative Analyst**: Stresses extreme volatility, regulatory uncertainty, security risks
- **Neutral Analyst**: Balances growth vs risk, suggests position sizing for volatility

### 3. CLI Improvements
- **Welcome Screen**: Now prominently mentions crypto support
- **Ticker Prompt**: Shows examples for both stocks and crypto
- **Asset Detection Display**: After entering a ticker, shows whether it's a stock or cryptocurrency with visual indicators (₿ for crypto, 📈 for stock)

## Usage Examples

### From CLI
```bash
python -m cli.main
# Enter "BTC" when prompted for ticker
# You'll see: "₿ Detected asset type: CRYPTOCURRENCY"
```

### From Python
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["crypto_settings"]["default_market"] = "USD"

ta = TradingAgentsGraph(debug=True, config=config)

# Analyze Bitcoin - automatically detects crypto and uses crypto-specific prompts
_, decision = ta.propagate("BTC", "2024-05-10")
print(decision)
```

## Testing
Run the test suite to verify crypto-specific functionality:
```bash
python test_crypto_prompts.py
```

Tests verify:
1. Asset type detection works correctly for both crypto and stock symbols
2. State initialization includes `asset_type` field
3. All agent functions are accessible

## Key Design Principles

1. **Backward Compatible**: Stock analysis works exactly as before. Crypto-specific logic only activates when analyzing crypto.

2. **Minimal Changes**: Core architecture unchanged. Only prompts are enhanced based on asset type.

3. **Automatic Detection**: Users don't need to specify whether analyzing crypto or stock - system detects automatically.

4. **Comprehensive Coverage**: Every agent in the pipeline (from analysts to risk management) has crypto-specific guidance.

## Future Enhancements
Potential areas for improvement:
- Add crypto-specific tools for on-chain metrics
- Integrate with crypto-specific data providers (CoinGecko, etc.)
- Add crypto-specific risk metrics (volatility measures, liquidity scores)
- Support for DeFi protocols and NFT analysis
