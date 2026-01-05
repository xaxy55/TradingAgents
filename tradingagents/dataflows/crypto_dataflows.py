"""
Cryptocurrency data providers for TradingAgents.

This module provides data fetching functions for cryptocurrency markets,
supporting multiple data sources including Alpha Vantage, CoinGecko, and others.
"""

from typing import Annotated
from datetime import datetime
from .alpha_vantage_common import _make_api_request
import pandas as pd
from io import StringIO


def get_crypto_price_alpha_vantage(
    symbol: Annotated[str, "Cryptocurrency symbol (e.g., BTC, ETH)"],
    market: Annotated[str, "Market/fiat currency (e.g., USD, EUR)"] = "USD",
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"] = None,
    end_date: Annotated[str, "End date in yyyy-mm-dd format"] = None,
) -> str:
    """
    Retrieve cryptocurrency price data (OHLCV) from Alpha Vantage.
    
    Uses Alpha Vantage's DIGITAL_CURRENCY_DAILY endpoint to get daily
    time series data for digital currencies.
    
    Args:
        symbol: Cryptocurrency symbol (e.g., BTC, ETH, LTC)
        market: Market/fiat currency (default: USD)
        start_date: Start date for filtering (optional)
        end_date: End date for filtering (optional)
    
    Returns:
        str: CSV-formatted string containing OHLCV data
    """
    params = {
        "symbol": symbol.upper(),
        "market": market.upper(),
    }
    
    # Alpha Vantage uses DIGITAL_CURRENCY_DAILY for crypto
    csv_data = _make_api_request("DIGITAL_CURRENCY_DAILY", params)
    
    # Check if we got valid data
    if not csv_data or csv_data.strip() == "":
        return f"No data available for {symbol}/{market}"
    
    # Filter by date range if provided
    if start_date and end_date:
        try:
            df = pd.read_csv(StringIO(csv_data))
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                start_dt = pd.to_datetime(start_date)
                end_dt = pd.to_datetime(end_date)
                df = df[(df['timestamp'] >= start_dt) & (df['timestamp'] <= end_dt)]
                csv_data = df.to_csv(index=False)
        except Exception as e:
            print(f"Warning: Could not filter crypto data by date: {e}")
    
    # Add header information
    header = f"# Cryptocurrency data for {symbol.upper()}/{market.upper()}\n"
    if start_date and end_date:
        header += f"# Date range: {start_date} to {end_date}\n"
    header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    return header + csv_data


def get_crypto_intraday_alpha_vantage(
    symbol: Annotated[str, "Cryptocurrency symbol (e.g., BTC, ETH)"],
    market: Annotated[str, "Market/fiat currency (e.g., USD, EUR)"] = "USD",
    interval: Annotated[str, "Time interval (1min, 5min, 15min, 30min, 60min)"] = "60min",
) -> str:
    """
    Retrieve intraday cryptocurrency price data from Alpha Vantage.
    
    Args:
        symbol: Cryptocurrency symbol (e.g., BTC, ETH, LTC)
        market: Market/fiat currency (default: USD)
        interval: Time interval for intraday data
    
    Returns:
        str: CSV-formatted string containing intraday OHLCV data
    """
    params = {
        "symbol": symbol.upper(),
        "market": market.upper(),
        "interval": interval,
    }
    
    csv_data = _make_api_request("CRYPTO_INTRADAY", params)
    
    # Check if we got valid data
    if not csv_data or csv_data.strip() == "":
        return f"No intraday data available for {symbol}/{market} at {interval} interval"
    
    # Add header information
    header = f"# Intraday cryptocurrency data for {symbol.upper()}/{market.upper()}\n"
    header += f"# Interval: {interval}\n"
    header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    return header + csv_data


def get_crypto_market_overview(
    crypto_list: Annotated[list[str], "List of cryptocurrency symbols"] = None,
) -> str:
    """
    Get market overview for major cryptocurrencies.
    
    This is a placeholder for aggregating crypto market data.
    Can be extended to use CoinGecko, CoinMarketCap, or other APIs.
    
    Args:
        crypto_list: Optional list of specific cryptos to track (e.g., ["BTC", "ETH"])
    
    Returns:
        str: Market overview data
    """
    if crypto_list is None:
        crypto_list = ["BTC", "ETH"]
    
    # For now, return a formatted message
    # This can be extended to actually fetch from external APIs
    return f"Market overview for: {', '.join(crypto_list)}\nNote: Extend this function with CoinGecko or similar API for live market data."


def is_crypto_symbol(symbol: str) -> bool:
    """
    Detect if a symbol is likely a cryptocurrency.
    
    Uses heuristics to determine if the given symbol represents
    a cryptocurrency rather than a stock.
    
    Args:
        symbol: Trading symbol to check
    
    Returns:
        bool: True if likely a cryptocurrency, False otherwise
    """
    # Common cryptocurrency symbols
    crypto_symbols = {
        'BTC', 'ETH', 'USDT', 'BNB', 'USDC', 'XRP', 'ADA', 'DOGE',
        'SOL', 'TRX', 'DOT', 'MATIC', 'LTC', 'SHIB', 'AVAX', 'UNI',
        'LINK', 'XLM', 'ATOM', 'XMR', 'ETC', 'BCH', 'APT', 'FIL',
        'NEAR', 'VET', 'ALGO', 'HBAR', 'ICP', 'QNT', 'CRO', 'LDO',
    }
    
    symbol_upper = symbol.upper()
    
    # Check if it's in our known crypto list
    if symbol_upper in crypto_symbols:
        return True
    
    # Check for common crypto suffixes/patterns
    # Some exchanges use suffixes like BTCUSD, ETHUSD
    for crypto in crypto_symbols:
        if symbol_upper.startswith(crypto) and len(symbol_upper) > len(crypto):
            return True
    
    return False
