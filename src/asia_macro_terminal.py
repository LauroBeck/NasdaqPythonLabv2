import yfinance as yf
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

ASSETS = {
    "KOSPI": "^KS11",
    "KOSDAQ": "^KQ11",
    "NIKKEI 225": "^N225",
    "HANG SENG": "^HSI",
    "NIFTY 50": "^NSEI",
    "USDJPY": "JPY=X",
    "USDKRW": "KRW=X",
    "US10Y": "^TNX"
}

def fetch_market():

    results = {}

    for name, ticker in ASSETS.items():

        try:
            ticker_obj = yf.Ticker(ticker)
            data = ticker_obj.history(period="5d")

            if data.empty:
                results[name] = None
                continue

            close = data["Close"].dropna()

            if len(close) < 2:
                results[name] = None
                continue

            last = float(close.iloc[-1])
            prev = float(close.iloc[-2])

            change = last - prev
            pct = (change / prev) * 100

            results[name] = (last, change, pct)

        except Exception:
            results[name] = None

    return results


def display_terminal(data):

    table = Table(title="BLOOMBERG ASIA MARKET CHECK")

    table.add_column("Asset")
    table.add_column("Price", justify="right")
    table.add_column("Change", justify="right")
    table.add_column("Change %", justify="right")

    for asset, values in data.items():

        if values is None:
            table.add_row(asset, "N/A", "-", "-")
            continue

        price, change, pct = values

        color = "green" if change >= 0 else "red"

        table.add_row(
            asset,
            f"{price:,.2f}",
            f"[{color}]{change:,.2f}[/{color}]",
            f"[{color}]{pct:.2f}%[/{color}]"
        )

    console.print()
    console.print("Time:", datetime.now())
    console.print(table)


if __name__ == "__main__":

    data = fetch_market()
    display_terminal(data)
