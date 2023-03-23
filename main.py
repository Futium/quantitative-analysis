import config
import movingaverage

ticker_list = ['AAPL', 'MSFT']

if config.auto == False:
    ### get historical data
    ticker = input("What Ticker are you seeking analysis on?\n").upper()

else:
    for ticker in ticker_list:
        movingaverage.main(ticker)


