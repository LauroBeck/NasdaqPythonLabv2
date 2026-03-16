import yfinance as yf
import pandas as pd
from datetime import datetime


def get_market_data(tickers=None, start="2024-01-01", end=None):

    if tickers is None:
        tickers = [
            "AAPL",
            "MSFT",
            "NVDA",
            "AMZN",
            "GOOGL",
            "META",
            "TSLA"
        ]

    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    print("\nDownloading NASDAQ market data...")

    data = yf.download(
        tickers,
        start=start,
        end=end,
        group_by="ticker",
        auto_adjust=True
    )

    print("Download complete.")

    return data


def extract_close_prices(data):

    closes = {}

    for ticker in data.columns.levels[0]:
        closes[ticker] = data[ticker]["Close"]

    df = pd.DataFrame(closes)

    return df
