import pandas as pd

from market_regime_engine import MarketRegimeEngine
from macro_liquidity_engine import MacroLiquidityEngine
from volatility_risk_engine import VolatilityRiskEngine


class MacroAITerminal:

    def __init__(self):

        self.regime_engine = MarketRegimeEngine()
        self.liquidity_engine = MacroLiquidityEngine()
        self.vol_engine = VolatilityRiskEngine()


    def run(self):

        print("\n==============================")
        print("GLOBAL MACRO AI TERMINAL")
        print("==============================\n")


        # MARKET REGIME
        print("Loading Market Regime Engine...\n")

        regime_df = self.regime_engine.load_macro_data()

        if not regime_df.empty:

            regime_changes = self.regime_engine.compute_daily_changes(regime_df)

            regime = self.regime_engine.detect_regime(regime_changes)

        else:

            regime = "Unknown"


        # LIQUIDITY ENGINE
        print("Loading Liquidity Engine...\n")

        liq_df = self.liquidity_engine.load_data()

        if not liq_df.empty:

            score, returns = self.liquidity_engine.compute_liquidity_score(liq_df)

            liquidity_regime = self.liquidity_engine.classify_liquidity(score)

        else:

            liquidity_regime = "Unknown"


        # VOLATILITY ENGINE
        print("Loading Volatility Engine...\n")

        vol_df = self.vol_engine.load_data()

        if not vol_df.empty:

            vol_signal = self.vol_engine.compute_volatility_signal(vol_df)

        else:

            vol_signal = "Unknown"


        # DASHBOARD OUTPUT
        print("\n==============================")
        print("MACRO MARKET DASHBOARD")
        print("==============================\n")

        print("Market Regime:", regime)

        print("Liquidity Regime:", liquidity_regime)

        print("Volatility Signal:", vol_signal)

        print("\n==============================\n")


if __name__ == "__main__":

    terminal = MacroAITerminal()

    terminal.run()
