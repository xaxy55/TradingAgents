"""
Cryptocurrency-specific tools for TradingAgents.

This module provides LangChain tools that agents can use to analyze
cryptocurrency markets.
"""

from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor
from tradingagents.dataflows.crypto_dataflows import is_crypto_symbol


@tool
def get_crypto_price(
    symbol: Annotated[str, "Cryptocurrency symbol (e.g., BTC, ETH)"],
    market: Annotated[str, "Market/fiat currency (e.g., USD, EUR)"] = "USD",
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"] = None,
    end_date: Annotated[str, "End date in yyyy-mm-dd format"] = None,
) -> str:
    """
    Retrieve cryptocurrency price data (OHLCV) for analysis.
    
    This tool fetches historical or current price data for cryptocurrencies
    from configured data providers.
    
    Args:
        symbol: Cryptocurrency symbol (e.g., BTC for Bitcoin, ETH for Ethereum)
        market: The fiat or stablecoin market pair (default: USD)
        start_date: Optional start date for historical data
        end_date: Optional end date for historical data
    
    Returns:
        str: Formatted price data including open, high, low, close, volume
    
    Examples:
        - Get Bitcoin price in USD: get_crypto_price("BTC", "USD")
        - Get Ethereum historical data: get_crypto_price("ETH", "USD", "2024-01-01", "2024-01-31")
    """
    return route_to_vendor("get_crypto_price", symbol, market, start_date, end_date)


@tool
def get_crypto_intraday(
    symbol: Annotated[str, "Cryptocurrency symbol (e.g., BTC, ETH)"],
    market: Annotated[str, "Market/fiat currency (e.g., USD, EUR)"] = "USD",
    interval: Annotated[str, "Time interval (1min, 5min, 15min, 30min, 60min)"] = "60min",
) -> str:
    """
    Retrieve intraday cryptocurrency price data for short-term analysis.
    
    This tool is useful for day trading and technical analysis that requires
    granular time intervals.
    
    Args:
        symbol: Cryptocurrency symbol
        market: The fiat or stablecoin market pair
        interval: Time interval between data points
    
    Returns:
        str: Intraday price data with specified interval
    
    Examples:
        - Get hourly BTC data: get_crypto_intraday("BTC", "USD", "60min")
        - Get 5-minute ETH data: get_crypto_intraday("ETH", "USD", "5min")
    """
    return route_to_vendor("get_crypto_intraday", symbol, market, interval)


@tool 
def detect_asset_type(
    symbol: Annotated[str, "Trading symbol to analyze"],
) -> str:
    """
    Detect whether a trading symbol represents a cryptocurrency or traditional stock.
    
    This tool helps agents determine the appropriate analysis approach based on
    the asset type.
    
    Args:
        symbol: Trading symbol to check
    
    Returns:
        str: "cryptocurrency" or "stock"
    
    Examples:
        - detect_asset_type("BTC") returns "cryptocurrency"
        - detect_asset_type("AAPL") returns "stock"
    """
    if is_crypto_symbol(symbol):
        return "cryptocurrency"
    else:
        return "stock"
