import yfinance as yf

ticker = input("What Ticker are you seeking analysis on?\n").upper()

data = yf.download(ticker, interval='1m')

print(data)

print(yf.Ticker(ticker).fast_info['lastPrice'])