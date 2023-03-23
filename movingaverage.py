import yfinance as yf
import pandas as pd
import time
from termcolor import colored
import numpy as np
from datetime import date
from pprint import pprint
import os
import config
import historical_data

# get time 
t = time.localtime()

# get today's date
today = date.today()

### get historical data
ticker = input("What Ticker are you seeking analysis on?\n").upper()

k = config.k
eval_len = config.eval_len
prec_lvl = config.prec_lvl
csv_save_location = config.csv_save_location
performance_folder = config.performance_folder
performance_figures_folder = config.performance_figures_folder
data_date = config.data_date

# what the file name should be 
filename = 'k_of_' + str(k) + '_historicalRecord_for_' + ticker + '_on_' + str(data_date) + '.csv'

# grab the data whether historical or present
df = historical_data.get_historical_data(ticker)

# check if the dataframe is empty
if df.empty:
    quit()

lastPrice_historical = df['mean']

# iterations
# do all data
iterations = len(df['mean'])

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
        time.sleep(0.0001)


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

    df_new = df2[df2['Action'].notna()]

    grp = (df_new['Action'] == 'SELL').cumsum().shift().bfill()

    dd = dict(tuple(df_new.groupby(grp)))

    list_of_dfs = [g for _, g in dd.items() if len(g) > 1]

    buy_price = []
    price = []
    sell_price = []
    pct_gain = []
    moving_average = []
    action = []
    current_time = []

    ### len of list_of_dfs is # of subtables 
    for n in range(len(list_of_dfs)):
        ###(list with all the data[subtable number]['Column Name'].iloc[nth row])
        buy_price.append(list_of_dfs[n]['Price'].iloc[0])
        sell_price.append(list_of_dfs[n]['Price'].iloc[-1])

        ## get values for performance figures and use extend to add them to the list
        current_time.extend(list_of_dfs[n]['Current Time'].tolist())
        price.extend(list_of_dfs[n]['Price'].tolist())
        moving_average.extend(list_of_dfs[n]['Moving Average'].tolist())
        action.extend(list_of_dfs[n]['Action'].tolist())

        pct_gain.append(100 * (sell_price[n] - buy_price[n]) / buy_price[n])
    total_gain = str(sum(pct_gain)) + '%' 

    ### take the performance and get them into a .csv file
    # find the performance and make them into a table
    gain_values = [[total_gain]]
    performance = pd.DataFrame(gain_values, columns=['Total Gain:'])

    # create file name for performance
    performance_file_name = 'performance_with_for_' + ticker + '_k_of_' + str(k) + '_on_' + str(data_date) + '.csv'

    # save to csv
    performance.to_csv(os.path.join(performance_folder, performance_file_name))

    # print(current_time)

    ### take the subtables and make them into a dataframe
    columns = ['Current Time', 'Price', 'Moving Average', 'Action']
    data = pd.DataFrame(columns=columns)

    ### set the columns = to the lists
    data['Current Time'] = current_time
    data['Price'] = price
    data['Moving Average'] = moving_average
    data['Action'] = action

    # create performance figures file name
    performance_figures_file_name = 'performance_figures_with_eval_len_' + '_k_of_' + str(k) + '_on_' + str(data_date) + '.csv'

    # save to csv
    data.to_csv(os.path.join(performance_figures_folder, performance_figures_file_name))


if __name__ == "__main__":
    main()
