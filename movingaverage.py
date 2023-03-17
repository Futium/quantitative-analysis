import yfinance as yf
import pandas as pd
import time
from termcolor import colored
import numpy as np
from datetime import date

### get historical data
ticker = input("What Ticker are you seeking analysis on?\n").upper()

data = yf.download(ticker, period='1d', interval='1m', prepost=True)

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
times = len(df['mean'])


# value of k for moving average
k = 10

t = time.localtime()
ticker_price = []
change = []
current_time = []
pct_change = []

def get_price_and_price(x):
    ticker_price.append(lastPrice_historical[x])

    current_time.append(time.strftime("%H:%M:%S", t))

    change.append((ticker_price[x] - ticker_price[x-1]))

    pct_change.append(change[x] / ticker_price[x-1])

    if x == 0:
        return 0
    elif change[x] > 0:
        print('Price: ' + colored(str(round(ticker_price[x], 5)), 'green'))
        # print("\n    Change: ", colored(str(round(change[x], 6)), 'green'))
    elif change[x] < 0:
        print('Price: ' + colored(str(round(ticker_price[x], 5)), 'red'))
        # print("\n    Change: ", colored(str(round(change[x], 6)), 'red'))
    else: 
        print('Price: ' + colored(str(round(ticker_price[x], 5)), 'grey'))
        # print("\n    Change: ", colored(str(round(change[x], 6)), 'grey'))
    
    if x >= 10:
        get_moving_average(ticker_price, x)

    # if ticker_price[x] > ticker_price[0]:
    #     print(colored("            Up for Period", 'green'))
    # elif ticker_price[x] < ticker_price[0]:
    #     print(colored("            Down for Period", 'red'))
    # else:
    #     print(colored("            --", 'grey'))

    ### acceleration
    # acceleration = abs(pct_change[x] - pct_change[x-1])

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
    for x in range(times):
        get_price_and_price(x)
        time.sleep(0.001)
    price_ma_actions = pd.DataFrame(columns=['Current Time', 'Price', 'Moving Average', 'Action'])
    price_ma_actions['Current Time'] = current_time
    price_ma_actions['Price'] = ticker_price
    price_ma_actions['Moving Average'] = list_ma
    price_ma_actions['Action'] = action

    today = date.today()

    price_ma_actions.to_csv('historicalRecord_for_' + ticker + '_on_' + str(today) + '.csv')


list_ma = []
remaining = []
action = []
for i in range(k):
    list_ma.append(0)
for i in range(k):
    action.append(0)

def get_moving_average(ticker_price, x):
    df = pd.DataFrame(ticker_price)
    # exponential moving average
    moving_avg_ewm = df.ewm(k).mean().iloc[-1].values

    ## round moving average to nearest 5 dec
    rounded = round(moving_avg_ewm[0], 5)

    #make first k slots empty

    # add list of ma's
    list_ma.append(rounded)

    print(colored('MA: ' + str(rounded) + '\n', 'blue'))

    if rounded > ticker_price[x]:
        action.append("BUY")
        print(colored("BUY", 'green'))
    elif rounded < ticker_price[x]:
        action.append("SELL")
        print(colored("SELL", 'red'))
    else:
        action.append("-----")
        print("-----")

if __name__ == "__main__":
    main()

# df.to_csv(ticker + '.csv')

