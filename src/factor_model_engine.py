import pandas as pd
import yfinance
import numpy as np


class FactorModelEngine:

    def __init__(self):

        self.tickers = {
            "SP500": "^GSPC",
            "NASDAQ": "^IXIC",
            "APPLE": "AAPL",
            "MICROSOFT": "MSFT",
            "NVIDIA": "NVDA",
            "VIX": "^VIX"
        }


    def load_data(self):

        frames = []

        for name, ticker in self.tickers.items():

            try:

                print(f"Loading {name} ({ticker})")

                t = yfinance.Ticker(ticker)

                hist = t.history(period="6mo")

                if hist.empty:
                    continue

                series = hist["Close"].rename(name)

                frames.append(series)

                print(name, "rows:", len(series))

            except Exception as e:

                print("Error:", e)


        if len(frames) == 0:
            return pd.DataFrame()


        df = pd.concat(frames, axis=1)

        df.index = pd.to_datetime(df.index).date

        df = df.groupby(df.index).last()

        df = df.ffill()

        return df


    def momentum_factor(self, df):

        scores = {}

        for col in df.columns:

            if col == "VIX":
                continue

            m20 = df[col].pct_change(20).iloc[-1]

            m60 = df[col].pct_change(60).iloc[-1]

            scores[col] = float((m20 + m60) / 2)

        return scores


    def volatility_factor(self, df):

        vol = {}

        returns = df.pct_change()

        for col in df.columns:

            if col == "VIX":
                continue

            v = returns[col].rolling(20).std().iloc[-1]

            vol[col] = float(-v)

        return vol


    def risk_factor(self, df):

        vix = df["VIX"].iloc[-1]

        risk_score = 1

        if vix > 30:
            risk_score = -1

        if vix > 40:
            risk_score = -2

        return risk_score


    def combine_factors(self, momentum, volatility, risk):

        combined = {}

        for asset in momentum.keys():

            combined[asset] = momentum[asset] + volatility[asset] + risk * 0.01

        return combined


    def rank_assets(self, scores):

        ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return ranking


if __name__ == "__main__":

    print("\nMULTI FACTOR MODEL ENGINE\n")

    engine = FactorModelEngine()

    df = engine.load_data()

    if df.empty:

        print("No data loaded")

    else:

        print("\nLatest Market Data\n")

        print(df.tail())

        momentum = engine.momentum_factor(df)

        volatility = engine.volatility_factor(df)

        risk = engine.risk_factor(df)

        scores = engine.combine_factors(momentum, volatility, risk)

        ranking = engine.rank_assets(scores)

        print("\nMomentum Factor\n")

        print(momentum)

        print("\nVolatility Factor\n")

        print(volatility)

        print("\nRisk Score:", risk)

        print("\nFinal Factor Scores\n")

        print(scores)

        print("\nFactor Ranking\n")

        print(ranking)
