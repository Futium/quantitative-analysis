import yfinance as yf
import pandas as pd
import time
from termcolor import colored
import numpy as np
from datetime import date
from pprint import pprint

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
k = 5

# window of evaluation (i.e. how many data points do we wait until it materializes)
eval_len = 3

# how precise we want our numbers
prec_lvl = 5


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


    # 
    price_ma_actions.to_csv('k_of_' + str(k) + '_historicalRecord_for_' + ticker + '_on_' + str(today) + '.csv')

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
    df2 = pd.read_csv('k_of_' + str(k) + '_historicalRecord_for_' + ticker + '_on_' + str(today) + '.csv')

    df2 = df2.iloc[k:]
    df2 = df2.drop('Unnamed: 0', axis=1)
    # df2 = df2.reset_index(drop=True)

    # print(df2)

    desired_action = "BUY"


    eval_len = 3
    
    price0 = [window['Price'].iloc[0] for window in df2.rolling(window=eval_len)
           if len(window) == eval_len and window['Action'].iloc[0] == desired_action]
    price1 = [window['Price'].iloc[1] for window in df2.rolling(window=eval_len)
           if len(window) == eval_len and window['Action'].iloc[0] == desired_action]
    price2 = [window['Price'].iloc[eval_len-1] for window in df2.rolling(window=eval_len)
           if len(window) == eval_len and window['Action'].iloc[0] == desired_action]

    # new = pd.DataFrame(out, columns=['', 'Current Time', 'Price', 'Moving Average', 'Action'])

    # out = pd.DataFrame(out)

    # out.to_csv('out.csv')

    columns = []

    prices = []

    for num in range(eval_len):
        prices.append([window['Price'].iloc[num] for window in df2.rolling(window=eval_len)
           if len(window) == eval_len and window['Action'].iloc[0] == desired_action])
        columns.append("Price" + str(num))

    data = pd.DataFrame(columns=columns)

    for num in range(eval_len):
        data.iloc[:, num] = prices[num]

    # data['Price0'] = price0
    # data['Price1'] = price1
    # data['Price2'] = price2



    print(data)

    data.to_csv('dataTable.csv')

    # pprint()


if __name__ == "__main__":
    main()

# df.to_csv(ticker + '.csv')

