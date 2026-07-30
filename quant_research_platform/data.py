from __future__ import annotations

import pandas as pd
import yfinance as yf


def download_stock_data(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """Download adjusted close prices for a list of tickers."""
    data = yf.download(tickers, start=start, end=end, progress=False, auto_adjust=True)
    if isinstance(data.columns, pd.MultiIndex):
        data = data["Close"]
    return data
