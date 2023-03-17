import yfinance as yf
import pandas as pd

ticker = input("What Ticker are you seeking analysis on?\n").upper()

data = yf.download(ticker, interval='1m')

df = pd.DataFrame(data)

df[]

df.to_csv('df.csv')

print(data)

print(yf.Ticker(ticker).fast_info['lastPrice'])