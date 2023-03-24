import config
import pandas as pd
import os
import yfinance as yf
from datetime import date
from datetime import datetime
from datetime import timedelta
import naming

csv_save_location = config.csv_save_location


# get today's date
today = date.today()

def get_historical_data(ticker):
    filename = naming.filename(ticker)

    # date for the data we are looking for
    if config.data_date.lower() != 'today':
        data_date = config.data_date
        # convert string to datetime.date object
        data_date = datetime.strptime(data_date, '%Y-%m-%d').date()
    else: 
        data_date = today
        
    # what the raw data file name should be 
    data_filename = 'raw-data-' + filename
    
    if config.currency.lower() == 'historical':
        # check if this file exists first. 
        if not os.path.isfile(os.path.join(csv_save_location, data_filename)):
            if (today - data_date).days <= 5:
                # get historical data 
                data = yf.download(ticker, start=data_date, end=data_date + timedelta(days=1), interval='1m', prepost=True)

                data.to_csv(os.path.join(csv_save_location, data_filename))

                return filter_data(data, filename)
            else:
                print("The ticker you selected is outside the date range, historical data can only be sourced from the last 5 days. Did you mean to choose today, " + str(today) + "?")

                # return FORMATTED nothing
                return pd.Series([], dtype=pd.StringDtype())
        else:
            # historical file data
            data = pd.read_csv(os.path.join(csv_save_location, data_filename))

            return filter_data(data, filename)
    else: 
        # today's data
        data = yf.download(ticker, period='1d', interval='1m', prepost=True)

        # save file to folder and filename
        data.to_csv(os.path.join(csv_save_location, data_filename))

        return filter_data(data, filename)
    
    

def filter_data(data, filename):

    df = pd.DataFrame(data)

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

    filtered_data_filename = 'filtered-data-' + filename

    df.to_csv(os.path.join(csv_save_location, filtered_data_filename))

    return df