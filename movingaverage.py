import pandas as pd
import time
from termcolor import colored
import os
import config
import historical_data
import naming
import evaluate

csv_save_location = config.csv_save_location
performance_folder = config.performance_folder
performance_figures_folder = config.performance_figures_folder

def get_price_and_price(x, df, k, change, ticker_price, current_time, list_ma, action):
    # get time 
    t = time.localtime()
    
    # check if the dataframe is empty
    if df.empty:
        quit()
    
    lastPrice_historical = df['mean']
    

    pct_change = []
    ticker_price.append(lastPrice_historical[x])

    current_time.append(time.strftime("%H:%M:%S", t))

    change.append((ticker_price[x] - ticker_price[x-1]))

    pct_change.append(change[x] / ticker_price[x-1])

    print('\n')
    if x == 0:
        return 0
    elif change[x] > 0:
        print('Price: ' + colored(str(round_prec(ticker_price[x])), 'green'))
        # print("\n    Change: ", colored(str(round(change[x], 6)), 'green'))
    elif change[x] < 0:
        print('Price: ' + colored(str(round_prec(ticker_price[x])), 'red'))
        # print("\n    Change: ", colored(str(round(change[x], 6)), 'red'))
    else: 
        print('Price: ' + colored(str(round_prec(ticker_price[x])), 'grey'))
        # print("\n    Change: ", colored(str(round(change[x], 6)), 'grey'))
    
    if x >= k:
        get_moving_average(ticker_price, x, k, list_ma, action)
    

def round_prec(x):
    return round(x, config.prec_lvl)

def main(ticker):
    ### initialize lists
    ticker_price = []
    current_time = []
    list_ma = []
    action = []
    change = []

    k = config.k

    # what the file name should be 
    filename = naming.filename(ticker)

    
    # grab the data whether historical or present
    df = historical_data.get_historical_data(ticker)
    
    ## iterations
    # do all data
    iterations = len(df['mean'])


    # set first k items in the list as blank for MA and Action since we wont have a data point for it
    for i in range(k):
        list_ma.append("")
    for i in range(k):
        action.append("")
    
    

    ### get price info 
    for x in range(iterations):
        get_price_and_price(x, df, k, change, ticker_price, current_time, list_ma, action)
        # # since the system only evaluating the past no need for sleep function
        # time.sleep(0.0001)


    # add the lists to the data table for price, ma, and actions
    price_ma_actions = pd.DataFrame(columns=['Current Time', 'Price', 'Moving Average', 'Action'])
    price_ma_actions['Current Time'] = current_time
    price_ma_actions['Price'] = ticker_price
    price_ma_actions['Moving Average'] = list_ma
    price_ma_actions['Action'] = action


    # save file to folder and filename
    price_ma_actions.to_csv(os.path.join(csv_save_location, filename))

    total_gain = evaluate.evaluate_performance(filename)

    return total_gain
    

def get_moving_average(ticker_price, x, k, list_ma, action):
    df = pd.DataFrame(ticker_price)
    # exponential moving average
    moving_avg_ewm = df.ewm(k).mean().iloc[-1].values

    ## round moving average to nearest 5 dec
    rounded = round_prec(moving_avg_ewm[0])

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
