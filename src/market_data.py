import yfinance as yf
import pandas as pd
from datetime import datetime


def get_market_data(tickers=None, start="2025-01-01", end=None, save_csv=False):

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

    print("\nDownloading NASDAQ data...")
    print("Tickers:", tickers)

    try:

        data = yf.download(
            tickers,
            start=start,
            end=end,
            group_by="ticker",
            auto_adjust=True
        )

        print("Download completed.")

        if save_csv:
            filename = "../data/nasdaq_market_data.csv"
            data.to_csv(filename)
            print("Saved to:", filename)

        return data

    except Exception as e:

        print("Data download error:", e)
        return pd.DataFrame()
