import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_prices(ticker: str, period: str = "1mo", interval: str = "1d") -> str:
    """
    Fetches historical stock prices for a given ticker.
    Args:
        ticker: The stock symbol (e.g., 'AAPL').
        period: The period of data to fetch (default '1mo').
        interval: The interval of data (default '1d').
    Returns:
        String representation of the dataframe.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        return df.to_string()
    except Exception as e:
        return f"Error fetching stock prices for {ticker}: {e}"

def get_financial_info(ticker: str) -> str:
    """
    Fetches basic financial information for a given ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # Extract key metrics to avoid token limit overflow with full dump
        key_metrics = {
            "symbol": info.get("symbol"),
            "longName": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "marketCap": info.get("marketCap"),
            "forwardPE": info.get("forwardPE"),
            "trailingPE": info.get("trailingPE"),
            "dividendYield": info.get("dividendYield"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
            "businessSummary": info.get("longBusinessSummary"),
        }
        return str(key_metrics)
    except Exception as e:
        return f"Error fetching financial info for {ticker}: {e}"
