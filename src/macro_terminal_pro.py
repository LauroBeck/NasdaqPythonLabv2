import yfinance as yf
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

ASSETS = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "NIKKEI 225": "^N225",
    "BRENT OIL": "BZ=F",
    "USDJPY": "JPY=X",
    "US10Y": "^TNX"
}

def fetch_market_data():

    results = {}

    for name, ticker_symbol in ASSETS.items():

        try:

            ticker = yf.Ticker(ticker_symbol)

            df = ticker.history(period="5d")

            if df.empty:
                results[name] = None
                continue

            closes = df["Close"].dropna()

            if len(closes) < 2:
                results[name] = None
                continue

            last = float(closes.iloc[-1])
            prev = float(closes.iloc[-2])

            change = last - prev
            pct = (change / prev) * 100

            results[name] = (last, change, pct)

        except Exception:
            results[name] = None

    return results


def display_terminal(data):

    table = Table(title="GLOBAL MACRO MARKET TERMINAL")

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


def main():

    data = fetch_market_data()
    display_terminal(data)


if __name__ == "__main__":
    main()
