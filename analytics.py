import pandas as pd
import datetime as dt
import yfinance as yf
from tabulate import tabulate
from pandas.tseries.holiday import USFederalHolidayCalendar
import yahoo_fin.stock_info as si
from collections import Counter

def main():
    # find output directory, or make it if DNE
    data_dir = "data"
    ticker_dir = "tickers"

    # tickers = pd.read_csv(ticker_dir + "/2023-03-03 E of ^GSPC.csv")
    # tickers_list = tickers[tickers.columns[1]].values.tolist()
    tickers_list = ['A', 'AAPL']
    index = '^GSPC'
    ticker_data = {}
    ticker_open = {}
    ticker_close = {}
    ticker_high = {}
    ticker_low = {}
    index_data = {}
    index_open = {}
    index_close = {}
    index_high = {}
    index_low = {}
    ticker_daily_beta = {}

    def high(mean):
        return mean.max()

    def low(mean):
        return mean.min()

    def open_at(mean):
        return mean.first()

    def close_at(mean):
        return mean.last()

    def compile_raw_index_data():
        index_table = pd.read_csv(data_dir + "/2023-03-03 " + index + ".csv")

        # convert datetime column to datetime format
        index_table["Datetime"] = pd.to_datetime(index_table["Datetime"])

        # grab only the columns we want
        index_dates_values = index_table[["Datetime", "Open", "High", "Low", "Close"]]

        # calculate the mean of each column
        index_mean = index_table.iloc[:, 1:5].mean(axis=1)

        index_dates_values = index_dates_values.assign(Mean=index_mean)

        # group by day
        index_by_day = index_dates_values.groupby(index_dates_values['Datetime'].dt.date)

        # save data to variable
        index_data = index_dates_values

        mean = index_by_day["Mean"]

        index_high = high(mean)

        index_low = low(mean)

        index_open = open_at(mean)

        index_close = close_at(mean)

    def compile_raw_ticker_data():
        x = 0
        for ticker in tickers_list:
            # ticker_file = str(ticker)
            ticker_table = pd.read_csv(data_dir + "/2023-03-03 " + ticker + ".csv")

            # convert datetime column to datetime format
            ticker_table["Datetime"] = pd.to_datetime(ticker_table["Datetime"])

            # grab only the columns we want
            ticker_dates_values = ticker_table[["Datetime", "Open", "High", "Low", "Close"]]

            # calculate the mean of each column
            ticker_mean = ticker_table.iloc[:, 1:5].mean(axis=1)

            ticker_dates_values = ticker_dates_values.assign(Mean=ticker_mean)

            # group by day
            ticker_by_day = ticker_dates_values.groupby(ticker_dates_values['Datetime'].dt.date)

            # save data to variable
            ticker_data["ticker{0}".format(x)] = ticker_dates_values

            mean = ticker_by_day["Mean"]

            ticker_high["ticker{0}".format(x)] = high(mean)

            ticker_low["ticker{0}".format(x)] = low(mean)

            ticker_open["ticker{0}".format(x)] = open_at(mean)

            ticker_close["ticker{0}".format(x)] = close_at(mean)

            ticker_daily_beta["ticker{0}".format(x)] = daily_beta(x)

            # print(ticker_daily_beta["ticker{0}".format(x)])
            x += 1

    def daily_beta(x):
        cl = Counter(ticker_close["ticker{0}".format(x)])

        print(cl)

        op = Counter(ticker_open["ticker{0}".format(x)])

        ticker_gain = cl - op

        # # abs(ticker_close - ticker_open) / ticker_open
        # index_gain = abs(index_close - index_open) / index_open
        return ticker_gain # / index_gain

    def individual_stock_data():
        # Find individual stock data
        stock_name = input("What stock's info are you looking for?\n").upper()

        if stock_name not in tickers_list:
            print("Stock " + stock_name + " is not in the S&P 500, please try again.\n")
            individual_stock_data()
        else:
            stock_name_place = "ticker" + str(tickers_list.index(stock_name))

            # return past 5 days of data
            print(ticker_data[stock_name_place])

            # return high per day for past 5 days
            print("High:\n",  ticker_high[stock_name_place])

            # return low per day for past 5 days
            print("Low:\n", ticker_low[stock_name_place])

            # return open per day for past 5 days
            print("Open\n", ticker_open[stock_name_place])

            # return close per day for past 5 days
            print("Close\n", ticker_close[stock_name_place])

    def convert_data_to_csv():
        for ticker in tickers_list:
            ticker_parquet = pd.read_parquet(data_dir + "/2023-03-03 " + ticker + ".parquet")
            ticker_parquet.to_csv(data_dir + "/2023-03-03 " + ticker + ".csv")

        ticker_parquet = pd.read_parquet(data_dir + "/2023-03-03 " + index + ".parquet")
        ticker_parquet.to_csv(data_dir + "/2023-03-03 " + index + ".csv")

    # convert_data_to_csv()

    compile_raw_ticker_data()
    compile_raw_index_data()


    # individual_stock_data()


if __name__ == "__main__":
    main()




# # calculate the mean of each column
        # ticker_mean = ticker_table.iloc[:, 1:5].mean(axis=1)
        #
        # ticker_data["ticker{0}".format(x)] = ticker_dates_values.assign(Mean=ticker_mean)