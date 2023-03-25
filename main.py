import config
from movingaverage import moving_avg
import yahoo_fin.stock_info as si
import eval_total_performance
import winsound


sp500 = si.tickers_sp500()

ticker_list =  sp500[:2] # sp500 

total_stock_gain = []

if config.auto == False:
    ### get historical data
    ticker = input("What Ticker are you seeking analysis on?\n").upper()

else:
    for ticker in ticker_list:
        total_stock_gain.append(moving_avg((ticker)))

eval_total_performance.ttl_performance(ticker_list)

frequency = 1500  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second
repeats = 3

for i in range(repeats):
    winsound.Beep(frequency-i*250, duration)