import pandas as pd
import yfinance


class AIMarketForecaster:

    def __init__(self):

        self.tickers = {
            "SP500": "^GSPC",
            "NASDAQ": "^IXIC",
            "OIL": "CL=F",
            "US10Y": "^TNX"
        }


    def load_market_data(self):

        frames = []

        for name, ticker in self.tickers.items():

            try:

                print(f"Loading {name} ({ticker})")

                ticker_obj = yfinance.Ticker(ticker)

                hist = ticker_obj.history(period="3mo")

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


    def compute_momentum(self, df):

        momentum = {}

        for col in ["SP500", "NASDAQ"]:

            m20 = df[col].pct_change(20).iloc[-1]

            m50 = df[col].pct_change(50).iloc[-1]

            momentum[col] = (m20 + m50) / 2

        return momentum


    def macro_factor_score(self, df):

        returns = df.pct_change().iloc[-1]

        score = 0

        if returns["OIL"] < 0:
            score += 1

        if returns["US10Y"] < 0:
            score += 1

        return score


    def predict_trend(self, momentum, macro_score):

        signal = {}

        for asset, mom in momentum.items():

            if mom > 0 and macro_score >= 1:
                signal[asset] = "Bullish"

            elif mom < 0 and macro_score == 0:
                signal[asset] = "Bearish"

            else:
                signal[asset] = "Neutral"

        return signal


if __name__ == "__main__":

    print("\nAI MARKET FORECASTER\n")

    engine = AIMarketForecaster()

    df = engine.load_market_data()

    if df.empty:

        print("No market data loaded")

    else:

        print("\nLatest Prices\n")

        print(df.tail())

        momentum = engine.compute_momentum(df)

        macro_score = engine.macro_factor_score(df)

        prediction = engine.predict_trend(momentum, macro_score)

        print("\nMomentum Signals\n")

        print(momentum)

        print("\nMacro Factor Score:", macro_score)

        print("\nAI Market Prediction\n")

        print(prediction)
