from langchain_core.tools import tool
from typing import Annotated

from tradingagents.dataflows.interface import route_to_vendor

@tool
def get_indicators(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[
        str | list[str],
        "technical indicator name (string) or list of indicator names",
    ],
    curr_date: Annotated[str, "The current trading date you are trading on, YYYY-mm-dd"],
    look_back_days: Annotated[int, "how many days to look back"] = 30,
) -> str:
    """
    Retrieve technical indicators for a given ticker symbol.
    Uses the configured technical_indicators vendor.
    Args:
        symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
        indicator (str): Technical indicator to get the analysis and report of
        curr_date (str): The current trading date you are trading on, YYYY-mm-dd
        look_back_days (int): How many days to look back, default is 30
    Returns:
        str: A formatted dataframe containing the technical indicators for the specified ticker symbol and indicator.
    """
    def _normalize_one(name: str) -> str:
        out = (name or "").strip()
        if out.startswith("boll_boll_"):
            out = out.replace("boll_boll_", "boll_", 1)
        elif out == "boll_boll":
            out = "boll"
        return out

    if isinstance(indicator, list):
        parts: list[str] = []
        for ind in indicator:
            normalized = _normalize_one(ind)
            if not normalized:
                continue
            parts.append(route_to_vendor("get_indicators", symbol, normalized, curr_date, look_back_days))
        return "\n\n".join(parts)

    normalized = _normalize_one(indicator)
    return route_to_vendor("get_indicators", symbol, normalized, curr_date, look_back_days)