import yfinance as yf
import pandas as pd

ticker = "AAPL"
data = yf.download(ticker, period="5d")

print("\nNASDAQ TEST DATA\n")
print(data)
