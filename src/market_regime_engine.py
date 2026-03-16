import yfinance as yf
import pandas as pd


class MarketRegimeEngine:

    def __init__(self):

        self.tickers = {
            "SP500": "^GSPC",
            "NASDAQ": "^IXIC",
            "OIL": "CL=F",
            "US10Y": "^TNX"
        }


    def load_macro_data(self):

        frames = []

        for name, ticker in self.tickers.items():

            try:

                print(f"Loading {name} ({ticker})")

                asset = yf.Ticker(ticker)

                hist = asset.history(period="1mo")

                print(f"{name} rows:", len(hist))

                if hist.empty:
                    continue

                series = hist["Close"].rename(name)

                frames.append(series)

            except Exception as e:

                print(f"Error loading {name}: {e}")


        if len(frames) == 0:
            return pd.DataFrame()


        df = pd.concat(frames, axis=1, sort=False)

        # normalize timestamps to trading dates
        df.index = pd.to_datetime(df.index).date

        # combine rows with same date
        df = df.groupby(df.index).last()

        # fill missing data
        df = df.ffill()

        return df


    def compute_daily_changes(self, df):

        returns = df.pct_change()

        return returns.iloc[-1]


    def detect_regime(self, changes):

        sp = changes.get("SP500", 0)
        oil = changes.get("OIL", 0)
        yield10 = changes.get("US10Y", 0)

        if sp > 0 and oil > 0 and yield10 > 0:
            return "Inflation / Risk-On"

        if sp < 0 and yield10 < 0:
            return "Deflation Risk"

        if sp < 0 and oil > 0:
            return "Stagflation Risk"

        return "Neutral"


if __name__ == "__main__":

    print("\nMACRO MARKET REGIME ENGINE\n")

    engine = MarketRegimeEngine()

    df = engine.load_macro_data()

    if df.empty:

        print("\nNo macro data loaded")

    else:

        print("\nLatest Macro Prices\n")

        print(df.tail())

        changes = engine.compute_daily_changes(df)

        print("\nDaily Macro Changes\n")

        print(changes)

        regime = engine.detect_regime(changes)

        print("\nDetected Market Regime\n")

        print(regime)
