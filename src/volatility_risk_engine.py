import pandas as pd
import yfinance


class VolatilityRiskEngine:

    def __init__(self):

        self.tickers = {
            "SP500": "^GSPC",
            "NASDAQ": "^IXIC",
            "VIX": "^VIX"
        }


    def load_data(self):

        frames = []

        for name, ticker in self.tickers.items():

            try:

                print(f"Loading {name} ({ticker})")

                ticker_obj = yfinance.Ticker(ticker)

                hist = ticker_obj.history(period="1mo")

                if hist.empty:
                    print("No data")
                    continue

                series = hist["Close"].rename(name)

                frames.append(series)

                print(name, "rows:", len(series))

            except Exception as e:

                print(f"Error loading {name}:", e)


        if len(frames) == 0:
            return pd.DataFrame()


        df = pd.concat(frames, axis=1, sort=False)

        df.index = pd.to_datetime(df.index).date

        df = df.groupby(df.index).last()

        df = df.ffill()

        return df


    def compute_volatility_signal(self, df):

        latest = df.iloc[-1]

        vix = latest["VIX"]

        if vix > 35:
            return "Market Panic"

        if vix > 25:
            return "High Volatility"

        if vix > 18:
            return "Moderate Risk"

        return "Calm Market"


if __name__ == "__main__":

    print("\nVOLATILITY RISK ENGINE\n")

    engine = VolatilityRiskEngine()

    df = engine.load_data()

    if df.empty:

        print("\nNo data loaded")

    else:

        print("\nLatest Market Prices\n")

        print(df.tail())

        signal = engine.compute_volatility_signal(df)

        print("\nVolatility Regime\n")

        print(signal)
