import yfinance as yf
import pandas as pd
import time
from termcolor import colored
import numpy as np
from datetime import date
from pprint import pprint
import os

# get time 
t = time.localtime()

# get today's date
today = date.today()

### get historical data
ticker = input("What Ticker are you seeking analysis on?\n").upper()

# if we want to get knew data
# data = yf.download(ticker, period='1d', interval='1m', prepost=True)
data = pd.read_csv(ticker + '.csv')

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


lastPrice_historical = df['mean']

### global variables
# iterations
# do all data
iterations = len(df['mean'])

# value of k for moving average
k = 3

# window of evaluation (i.e. how many data points do we wait until it materializes)
eval_len = 2

# how precise we want our numbers
prec_lvl = 5

# where CSV's will be saved
csv_save_location = 'CSVs'

# where performance bottomlines are saved
performance_folder = 'Performance'

# where performance figures are saved
performance_figures_folder = 'Performance Figures'


filename = 'k_of_' + str(k) + '_historicalRecord_for_' + ticker + '_on_' + str(today) + '.csv'

### initialize lists
change = []
ticker_price = []
current_time = []
list_ma = []
action = []

def get_price_and_price(x):
    pct_change = []
    ticker_price.append(lastPrice_historical[x])

    current_time.append(time.strftime("%H:%M:%S", t))

    change.append((ticker_price[x] - ticker_price[x-1]))

    pct_change.append(change[x] / ticker_price[x-1])

    print('\n')
    if x == 0:
        return 0
    elif change[x] > 0:
        print('Price: ' + colored(str(round(ticker_price[x], prec_lvl)), 'green'))
        # print("\n    Change: ", colored(str(round(change[x], 6)), 'green'))
    elif change[x] < 0:
        print('Price: ' + colored(str(round(ticker_price[x], prec_lvl)), 'red'))
        # print("\n    Change: ", colored(str(round(change[x], 6)), 'red'))
    else: 
        print('Price: ' + colored(str(round(ticker_price[x], prec_lvl)), 'grey'))
        # print("\n    Change: ", colored(str(round(change[x], 6)), 'grey'))
    
    if x >= k:
        get_moving_average(ticker_price, x)

    # if ticker_price[x] > ticker_price[0]:
    #     print(colored("            Up for Period", 'green'))
    # elif ticker_price[x] < ticker_price[0]:
    #     print(colored("            Down for Period", 'red'))
    # else:
    #     print(colored("            --", 'grey'))
    #
    ### acceleration
    # acceleration = abs(pct_change[x] - pct_change[x-1])
    #
    # if (acceleration > 0) and (pct_change[x] > 0):
    #     print("            ", colored(str(round(acceleration, 4)), 'green'))
    # elif (acceleration > 0) and (pct_change[x] < 0):
    #     print("            ", colored(str(round(acceleration, 4)), 'red'))
    # elif (acceleration < 0) and (pct_change[x] > 0):
    #     print("            ", colored(str(round(acceleration, 4)), 'green'))
    # elif (acceleration < 0) and (pct_change[x] < 0):
    #     print("            ", colored(str(round(acceleration, 4)), 'red'))
    # else:
    #     print(colored("            --", 'grey'))
    

def main():
    # set first k items in the list as blank for MA and Action since we wont have a data point for it
    for i in range(k):
        list_ma.append("")
    for i in range(k):
        action.append("")
    
    ### get price info
    for x in range(iterations):
        get_price_and_price(x)
        time.sleep(0.001)


    # add the lists to the data table for price, ma, and actions
    price_ma_actions = pd.DataFrame(columns=['Current Time', 'Price', 'Moving Average', 'Action'])
    price_ma_actions['Current Time'] = current_time
    price_ma_actions['Price'] = ticker_price
    price_ma_actions['Moving Average'] = list_ma
    price_ma_actions['Action'] = action


    # save file to folder and filename
    price_ma_actions.to_csv(os.path.join(csv_save_location, filename))

    evaluate_performance()
    



def get_moving_average(ticker_price, x):
    df = pd.DataFrame(ticker_price)
    # exponential moving average
    moving_avg_ewm = df.ewm(k).mean().iloc[-1].values

    ## round moving average to nearest 5 dec
    rounded = round(moving_avg_ewm[0], prec_lvl)

    #make first k slots empty

    # add list of ma's
    list_ma.append(rounded)

    print(colored('MA: ' + str(rounded), 'blue'))

    if rounded > ticker_price[x]:
        action.append("BUY")
        print(colored("BUY", 'green'))
    elif rounded < ticker_price[x]:
        action.append("SELL")
        print(colored("SELL", 'red'))
    else:
        action.append("-----")
        print("-----")
 

def evaluate_performance():
    df2 = pd.read_csv(csv_save_location + "/" + filename)

    df2 = df2.iloc[k:]
    df2 = df2.drop('Unnamed: 0', axis=1)

    desired_action = "BUY"
    
    columns_names = []

    prices = []

    comparison_point = 0

    # create list of column names
    for n in range(eval_len):
        columns_names.append('Price ' + str(n))

    # define column names from columns     
    data = pd.DataFrame(columns=columns_names)

    gain_table = pd.DataFrame()

    # create prices list and then add each array of prices to the column
    for n in range(eval_len):
        # get prices for each window each column is all the data for the nth value of the eval_len
        prices.append([window['Price'].iloc[n] for window in df2.rolling(window=eval_len)
           if len(window) == eval_len and window['Action'].iloc[0] == desired_action])
        
        # set each column equal to the nth price list
        data[data.columns[n]] = prices[n]

        if n != 0:
             # find the names of the price columns that we are looking for
            nth_column_name = data.columns[n]
            comparision_column_name = data.columns[comparison_point]
        
            # create the name of the column for the specific piece of data
            key_name = 'P ' + str(n) + ' - P ' + str(comparison_point)
            data[key_name] = data[nth_column_name] - data[comparision_column_name]
            
            # create a table with the gains from all of the stocks
            print(data[nth_column_name])
            print(data[comparision_column_name])
            gain_table[key_name] = 100 * (data[nth_column_name] - data[comparision_column_name]) / data[comparision_column_name]

    
    gain_table.to_csv('temp.csv')

    # find maximum of each row  
    data['Greatest Gain %'] = gain_table.max(axis=1)

    # find the column it occurred in
    data['Time of Success'] = gain_table.idxmax(axis=1)
        
    most_successful_time = data.mode()['Time of Success'][0]

    ### if we always made the right choice:
    perfect_ttl = str(round(data['Greatest Gain %'].sum(), prec_lvl)) + '%'

    print(key_name)

    ### total assuming you use the same method every time
    actual_ttl = str(round(gain_table[key_name].sum(), prec_lvl)) + '%'

    print(actual_ttl)

    print(perfect_ttl)

    # create performance figures file name
    performance_figures_file_name = 'performance_figures_with_eval_len_' + str(eval_len) + '_k_of_' + str(k) + '_on_' + str(today) + '.csv'

    # save to csv
    data.to_csv(os.path.join(performance_figures_folder, performance_figures_file_name))
    
    # find the performance figures and make them into a table
    values = [[most_successful_time, actual_ttl, perfect_ttl]]
    performance = pd.DataFrame(values, columns=['Most Frequent Row:', 'TTL Based on this Row:', 'Perfect Total:'])

    # create file name for performance
    performance_file_name = 'performance_with_eval_len_' + str(eval_len) + '_k_of_' + str(k) + '_on_' + str(today) + '.csv'

    # save to csv
    performance.to_csv(os.path.join(performance_folder, performance_file_name))

    # pprint()


if __name__ == "__main__":
    main()

# df.to_csv(ticker + '.csv')

