import pandas as pd
import numpy as np


def compute_returns(prices):

    returns = prices.pct_change().dropna()

    return returns


def compute_volatility(returns):

    volatility = returns.std() * np.sqrt(252)

    return volatility


def compute_momentum(prices, window=10):

    momentum = prices.pct_change(window)

    return momentum


def factor_score(returns, momentum):

    avg_return = returns.mean()

    mom = momentum.mean()

    score = avg_return + mom

    df = pd.DataFrame({
        'Return': avg_return,
        'Momentum': mom,
        'Score': score
    })

    df = df.sort_values("Score", ascending=False)

    return df
