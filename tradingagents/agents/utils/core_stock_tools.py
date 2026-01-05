from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor
from tradingagents.dataflows.crypto_dataflows import is_crypto_symbol


@tool
def get_stock_data(
    symbol: Annotated[str, "ticker symbol of the company or cryptocurrency"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve price data (OHLCV) for a given ticker symbol.
    Automatically detects if the symbol is a cryptocurrency or stock and routes to the appropriate data source.
    Uses the configured core_stock_apis vendor for stocks or cryptocurrency_data vendor for crypto.
    
    Note: For cryptocurrencies, this tool uses the default market setting from crypto_settings.default_market
    (typically USD). To specify a different market pair (e.g., EUR, GBP), use the get_crypto_price tool directly.
    
    Args:
        symbol (str): Ticker symbol, e.g. AAPL, TSM for stocks or BTC, ETH for cryptocurrencies
        start_date (str): Start date in yyyy-mm-dd format
        end_date (str): End date in yyyy-mm-dd format
    
    Returns:
        str: A formatted dataframe containing the price data for the specified ticker symbol in the specified date range.
    """
    # Detect if this is a cryptocurrency
    if is_crypto_symbol(symbol):
        # Get default market from config if available, otherwise use USD
        try:
            from tradingagents.dataflows.config import get_config
            config = get_config()
            market = config.get("crypto_settings", {}).get("default_market", "USD")
        except Exception:
            # Fallback to USD if config is not available
            market = "USD"
        
        # Route to crypto data provider
        return route_to_vendor("get_crypto_price", symbol, market, start_date, end_date)
    else:
        # Route to stock data provider
        return route_to_vendor("get_stock_data", symbol, start_date, end_date)
