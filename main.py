from movingaverage import moving_avg
import yahoo_fin.stock_info as si
import evaluate
from time import time
# import winsound

sp500 = si.tickers_sp500()

ticker_list = sp500[:2] # sp500 

total_stock_gain = []

iterations = 10

start_time = time()

for k in range(1, iterations+1):
        for ticker in ticker_list:
            total_stock_gain.append(moving_avg((ticker), k))
        evaluate.ttl_performance(ticker_list, k)

### no longer using this bc the if stmts could be slowing it down
# if config.auto == False:
#     ### get historical data
#     ticker = input("What Ticker are you seeking analysis on?\n").upper()

# else:
    
print(time() - start_time)