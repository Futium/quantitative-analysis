import config
from movingaverage import moving_avg
import yahoo_fin.stock_info as si
import eval_total_performance
import time
# import winsound


sp500 = si.tickers_sp500()

ticker_list =  sp500 # sp500 

total_stock_gain = []

start_time = time.time()

if config.auto == False:
    ### get historical data
    ticker = input("What Ticker are you seeking analysis on?\n").upper()

else:
    for ticker in ticker_list:
        total_stock_gain.append(moving_avg((ticker)))

print(time.time() - start_time)

eval_total_performance.ttl_performance(ticker_list)

# frequency = 1500  # Set Frequency To 2500 Hertz
# duration = 500  # Set Duration To 1000 ms == 1 second
# repeats = 3

# for i in range(repeats):
#     winsound.Beep(frequency-i*250, duration)