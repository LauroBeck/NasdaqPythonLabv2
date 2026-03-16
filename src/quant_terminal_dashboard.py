import time
from rich.console import Console
from rich.table import Table
from rich.live import Live

from market_regime_engine import MarketRegimeEngine
from macro_liquidity_engine import MacroLiquidityEngine
from volatility_risk_engine import VolatilityRiskEngine
from ai_market_forecaster import AIMarketForecaster
from portfolio_alpha_engine import PortfolioAlphaEngine
from factor_model_engine import FactorModelEngine


console = Console()


def build_dashboard():

    regime_engine = MarketRegimeEngine()
    liquidity_engine = MacroLiquidityEngine()
    vol_engine = VolatilityRiskEngine()
    ai_engine = AIMarketForecaster()
    alpha_engine = PortfolioAlphaEngine()
    factor_engine = FactorModelEngine()


    table = Table(title="GLOBAL QUANT MARKET TERMINAL")

    table.add_column("Module", style="cyan")
    table.add_column("Signal", style="green")


    try:

        regime_df = regime_engine.load_macro_data()

        if not regime_df.empty:

            changes = regime_engine.compute_daily_changes(regime_df)

            regime = regime_engine.detect_regime(changes)

        else:

            regime = "Unknown"

    except:

        regime = "Error"


    try:

        liq_df = liquidity_engine.load_data()

        if not liq_df.empty:

            score, _ = liquidity_engine.compute_liquidity_score(liq_df)

            liquidity = liquidity_engine.classify_liquidity(score)

        else:

            liquidity = "Unknown"

    except:

        liquidity = "Error"


    try:

        vol_df = vol_engine.load_data()

        if not vol_df.empty:

            vol_signal = vol_engine.compute_volatility_signal(vol_df)

        else:

            vol_signal = "Unknown"

    except:

        vol_signal = "Error"


    try:

        ai_df = ai_engine.load_market_data()

        if not ai_df.empty:

            momentum = ai_engine.compute_momentum(ai_df)

            macro = ai_engine.macro_factor_score(ai_df)

            prediction = ai_engine.predict_trend(momentum, macro)

        else:

            prediction = {}

    except:

        prediction = {}


    try:

        pf_df = alpha_engine.load_prices()

        if not pf_df.empty:

            scores = alpha_engine.compute_momentum_scores(pf_df)

            ranking = alpha_engine.rank_assets(scores)

            portfolio = alpha_engine.simulate_portfolio(ranking)

        else:

            portfolio = []

    except:

        portfolio = []


    try:

        factor_df = factor_engine.load_data()

        if not factor_df.empty:

            m = factor_engine.momentum_factor(factor_df)

            v = factor_engine.volatility_factor(factor_df)

            r = factor_engine.risk_factor(factor_df)

            combined = factor_engine.combine_factors(m, v, r)

            factor_rank = factor_engine.rank_assets(combined)

        else:

            factor_rank = []

    except:

        factor_rank = []


    table.add_row("Market Regime", str(regime))
    table.add_row("Liquidity", str(liquidity))
    table.add_row("Volatility", str(vol_signal))
    table.add_row("AI Forecast", str(prediction))
    table.add_row("Portfolio", str(portfolio))
    table.add_row("Factor Ranking", str(factor_rank[:3]))

    return table


if __name__ == "__main__":

    with Live(build_dashboard(), refresh_per_second=0.2) as live:

        while True:

            time.sleep(5)

            live.update(build_dashboard())
