import pandas as pd
import yfinance


class PortfolioAlphaEngine:

    def __init__(self):

        self.tickers = {
            "SP500": "^GSPC",
            "NASDAQ": "^IXIC",
            "APPLE": "AAPL",
            "MICROSOFT": "MSFT",
            "NVIDIA": "NVDA"
        }


    def load_prices(self):

        frames = []

        for name, ticker in self.tickers.items():

            try:

                print(f"Loading {name} ({ticker})")

                ticker_obj = yfinance.Ticker(ticker)

                hist = ticker_obj.history(period="6mo")

                if hist.empty:
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


    def compute_momentum_scores(self, df):

        scores = {}

        for col in df.columns:

            r20 = df[col].pct_change(20).iloc[-1]

            r60 = df[col].pct_change(60).iloc[-1]

            scores[col] = (r20 + r60) / 2

        return scores


    def rank_assets(self, scores):

        ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return ranking


    def simulate_portfolio(self, ranking):

        portfolio = []

        for asset, score in ranking[:3]:

            portfolio.append(asset)

        return portfolio


if __name__ == "__main__":

    print("\nPORTFOLIO ALPHA ENGINE\n")

    engine = PortfolioAlphaEngine()

    df = engine.load_prices()

    if df.empty:

        print("No market data loaded")

    else:

        print("\nLatest Prices\n")

        print(df.tail())

        scores = engine.compute_momentum_scores(df)

        ranking = engine.rank_assets(scores)

        portfolio = engine.simulate_portfolio(ranking)

        print("\nAlpha Scores\n")

        print(scores)

        print("\nAsset Ranking\n")

        print(ranking)

        print("\nSuggested Portfolio\n")

        print(portfolio)
