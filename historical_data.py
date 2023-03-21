import config
import pandas as pd
import os
import yfinance as yf
from datetime import date

csv_save_location = config.csv_save_location

# get today's date
today = str(date.today())



def get_historical_data(ticker):
    # date for the data we are looking for
    if config.data_date.lower() != 'today':
        data_date = config.data_date
    else: 
        data_date = today
        
    # what the raw data file name should be 
    data_filename = ticker + ' ' + data_date + '.csv'
    
    if config.currency.lower() == 'historical':
        # check if this file exists first. 
        if not os.path.isfile(os.path.join(csv_save_location, data_filename)):
            print("The ticker you selected with the date range does not exist, did you mean to choose today, " + today + "?")
            return False
        else:
            # historical file data
            data = pd.read_csv(os.path.join(csv_save_location, data_filename))
    else: 
        # today's data
        data = yf.download(ticker, period='1d', interval='1m', prepost=True)

        # save file to folder and filename
        data.to_csv(os.path.join(csv_save_location, data_filename))
    
    df = pd.DataFrame(data)

    df.index = df.index.astype(str)

    # drop all rows that include 4 AM, 5AM, 6AM, 7AM, 8AM, I'm not gonna be up at that time
    df = df[df.index.str.contains(" 04:") == False]
    df = df[df.index.str.contains(" 05:") == False]
    df = df[df.index.str.contains(" 06:") == False]
    df = df[df.index.str.contains(" 07:") == False]
    df = df[df.index.str.contains(" 08:") == False]
    df = df[df.index.str.contains(" 09:0") == False]
    df = df[df.index.str.contains(" 09:1") == False]
    df = df[df.index.str.contains(" 09:2") == False]

    # calculate mean
    df['mean'] = df.iloc[:, 1:5].mean(axis=1)

    return df
