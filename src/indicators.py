import pandas as pd
import numpy as np


def compute_returns(data):

    returns = {}

    for ticker in data.columns.levels[0]:

        close = data[ticker]["Close"]

        returns[ticker] = close.pct_change().dropna()

    df = pd.DataFrame(returns)

    return df



def compute_volatility(df):

    vol = df.std() * np.sqrt(252)

    return vol



def compute_momentum(df, window=5):

    momentum = df.rolling(window).mean()

    return momentum



def compute_sharpe(df):

    sharpe = df.mean() / df.std() * np.sqrt(252)

    return sharpe
