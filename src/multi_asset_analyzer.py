import pandas as pd
import numpy as np
from data_feed_engine import DataFeedEngine


class MultiAssetAnalyzer:

    def __init__(self):

        self.engine = DataFeedEngine()

    def compute_returns(self, df):

        return df.pct_change()

    def compute_momentum(self, df, window=5):

        return df.pct_change(window)

    def compute_volatility(self, df):

        returns = df.pct_change()

        return returns.std() * np.sqrt(252)

    def analyze(self):

        df = self.engine.load_prices()

        print("\nPRICE DATA\n")
        print(df.tail())

        returns = self.compute_returns(df)

        print("\nDAILY RETURNS\n")
        print(returns.tail())

        momentum = self.compute_momentum(df)

        print("\nMOMENTUM (5 DAY)\n")
        print(momentum.tail())

        vol = self.compute_volatility(df)

        print("\nANNUALIZED VOLATILITY\n")
        print(vol)


if __name__ == "__main__":

    analyzer = MultiAssetAnalyzer()

    analyzer.analyze()
