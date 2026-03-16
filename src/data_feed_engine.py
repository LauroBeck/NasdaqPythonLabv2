import yfinance as yf
import pandas as pd

class DataFeedEngine:

    def __init__(self):

        self.assets = {
            "SP500": "^GSPC",
            "NASDAQ": "^IXIC",
            "MSFT": "MSFT",
            "NVDA": "NVDA",
            "AAPL": "AAPL"
        }

    def load_prices(self):

        frames = []

        for name, ticker in self.assets.items():

            try:

                print(f"Loading {name} ({ticker})")

                ticker_obj = yf.Ticker(ticker)

                data = ticker_obj.history(period="1mo")

                if data.empty:
                    print(f"No data for {name}")
                    continue

                series = data["Close"].rename(name)

                frames.append(series)

            except Exception as e:

                print(f"Error loading {name}: {e}")

        if len(frames) == 0:
            return pd.DataFrame()

        df = pd.concat(frames, axis=1)

        return df


if __name__ == "__main__":

    print("\nNASDAQ PYTHON LAB DATA ENGINE\n")

    engine = DataFeedEngine()

    df = engine.load_prices()

    if df.empty:

        print("No market data loaded")

    else:

        print("\nMarket Data Snapshot\n")

        print(df.tail())
