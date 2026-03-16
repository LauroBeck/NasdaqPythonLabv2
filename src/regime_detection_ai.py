import numpy as np


def detect_market_regime(returns):

    market_mean = returns.mean().mean()
    market_vol = returns.std().mean()

    if market_mean > 0.001 and market_vol < 0.03:
        regime = "BULL"

    elif market_mean < -0.001:
        regime = "BEAR"

    elif market_vol > 0.04:
        regime = "HIGH VOLATILITY"

    else:
        regime = "SIDEWAYS"

    return regime, market_mean, market_vol
