import historical_data
import yahoo_fin.stock_info as si
import time

sp500 = si.tickers_sp500()

ticker_list = sp500

start_time = time.time()
for ticker in ticker_list:
    historical_data.get_historical_data(ticker)

print(time.time() - start_time)
