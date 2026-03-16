import yfinance as yf
from datetime import datetime

assets = {
    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
    "NIKKEI": "^N225",
    "BRENT": "BZ=F",
    "USDJPY": "JPY=X",
    "US10Y": "^TNX"
}

def get_market_data():

    results = {}

    for name, ticker in assets.items():

        try:
            df = yf.download(ticker, period="1d", interval="1m", progress=False)

            last = df["Close"].iloc[-1]
            first = df["Open"].iloc[0]

            change = last - first
            pct = (change / first) * 100

            results[name] = (last, change, pct)

        except:
            results[name] = (None, None, None)

    return results


def print_terminal(data):

    print()
    print("==============================")
    print("GLOBAL MACRO MARKET TERMINAL")
    print("==============================")
    print("Time:", datetime.now())
    print()

    for k,v in data.items():

        price, change, pct = v

        if price is None:
            print(f"{k:10} N/A")
            continue

        arrow = "" if change > 0 else ""

        print(f"{k:10} {price:10.2f} {arrow} {change:8.2f} ({pct:.2f}%)")


if __name__ == "__main__":

    data = get_market_data()
    print_terminal(data)
# Bloomberg style terminal
