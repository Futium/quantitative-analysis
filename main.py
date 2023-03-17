import yfinance as yf
import pandas as pd

ticker = input("What Ticker are you seeking analysis on?\n").upper()

data = yf.download(ticker, interval='1m', period='1d', prepost=True)

df = pd.DataFrame(data)

df.to_csv(ticker + '.csv')

# df = df[''df.Datetime ]

print(df)

print(yf.Ticker(ticker).fast_info['lastPrice'])