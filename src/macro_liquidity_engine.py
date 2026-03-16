import pandas as pd
import yfinance


class MacroLiquidityEngine:

    def __init__(self):

        self.tickers = {
            "SP500": "^GSPC",
            "NASDAQ": "^IXIC",
            "DXY": "DX-Y.NYB",
            "US10Y": "^TNX"
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


    def compute_liquidity_score(self, df):

        returns = df.pct_change().iloc[-1]

        score = 0

        if returns["SP500"] > 0:
            score += 1

        if returns["NASDAQ"] > 0:
            score += 1

        if returns["DXY"] < 0:
            score += 1

        if returns["US10Y"] < 0:
            score += 1

        return score, returns


    def classify_liquidity(self, score):

        if score >= 3:
            return "High Liquidity / Risk-On"

        if score == 2:
            return "Neutral Liquidity"

        return "Tight Liquidity / Risk-Off"


if __name__ == "__main__":

    print("\nMACRO LIQUIDITY ENGINE\n")

    engine = MacroLiquidityEngine()

    df = engine.load_data()

    if df.empty:

        print("\nNo data loaded")

    else:

        print("\nLatest Prices\n")

        print(df.tail())

        score, returns = engine.compute_liquidity_score(df)

        print("\nDaily Returns\n")

        print(returns)

        print("\nLiquidity Score:", score)

        regime = engine.classify_liquidity(score)

        print("\nLiquidity Regime\n")

        print(regime)
