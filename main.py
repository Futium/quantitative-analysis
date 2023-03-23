import config
import movingaverage
import yahoo_fin.stock_info as si

sp500 = si.tickers_sp500()

ticker_list = sp500

total_stock_gain = []

if config.auto == False:
    ### get historical data
    ticker = input("What Ticker are you seeking analysis on?\n").upper()

else:
    for ticker in ticker_list:
        total_stock_gain.append(movingaverage.main(ticker))

total_gain = sum(total_stock_gain)

print(total_gain)


