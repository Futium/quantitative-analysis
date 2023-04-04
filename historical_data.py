import config
import pandas as pd
import os.path
import yfinance as yf
from datetime import date
from datetime import datetime
from datetime import timedelta
import naming
import yahoo_fin.stock_info as si

save_location = config.save_location


# get today's date
today = date.today()

def get_historical_data(ticker):
    filename = naming.filename(ticker, 'raw')

    # date for the data we are looking for
    if config.data_date.lower() != 'today':
        data_date = config.data_date
        # convert string to datetime.date object
        data_date = datetime.strptime(data_date, '%Y-%m-%d').date()
    else: 
        data_date = today
        
    # what the raw data file name should be 
    data_filename = "".join(['raw-data-', filename])
    
    if config.currency.lower() == 'historical':
        # check if this file exists first. 
        if not os.path.isfile(os.path.join(save_location, data_filename)):
            if (today - data_date).days <= 5:
                # get historical data 
                data = yf.download(ticker, start=data_date, end=data_date + timedelta(days=1), interval='1m', prepost=True)

                data.to_parquet(os.path.join(save_location, data_filename))
            else:
                print("The ticker you selected is outside the date range, historical data can only be sourced from the last 5 days. Did you mean to choose today, " + str(today) + "?")
    else: 
        # today's data
        data = yf.download(ticker, period='1d', interval='1m', prepost=True)

        # save file to folder and filename
        data.to_parquet(os.path.join(save_location, data_filename))


def filter_data(ticker):
    filename = naming.filename(ticker, 'raw')

    # what the raw data file name should be 
    data_filename = "".join(['raw-data-', filename])
    
    df = pd.read_parquet(os.path.join(save_location, data_filename))

    df.index = df.index.astype(str)
    if config.pre_mrkt == False:
        # drop all rows that include 0400 , 0500, 0600, 0700, 0800, and up to 0930... I'm not gonna be up at that time
        df = df[df.index.str.contains(" 04:") == False]
        df = df[df.index.str.contains(" 05:") == False]
        df = df[df.index.str.contains(" 06:") == False]
        df = df[df.index.str.contains(" 07:") == False]
        df = df[df.index.str.contains(" 08:") == False]
        df = df[df.index.str.contains(" 09:0") == False]
        df = df[df.index.str.contains(" 09:1") == False]
        df = df[df.index.str.contains(" 09:2") == False]
    
    if config.post_mrkt == False:
        # drop all rows that include 1600, 1700, 1800, 1900... I'm don't want to work at that time
        df = df[df.index.str.contains(" 16:") == False]
        df = df[df.index.str.contains(" 17:") == False]
        df = df[df.index.str.contains(" 18:") == False]
        df = df[df.index.str.contains(" 19:") == False]
    

    # calculate mean
    df['mean'] = df.iloc[:, 1:5].mean(axis=1)

    filename = naming.filename(ticker, '')
    filtered_data_filename = "".join(['filtered-data-', filename])

    df.to_parquet(os.path.join(save_location, filtered_data_filename))

    return df


def main():
    sp500 = si.tickers_sp500()

    ticker_list = sp500

    for ticker in ticker_list:
        get_historical_data(ticker)


if __name__ == "__main__":
    main()