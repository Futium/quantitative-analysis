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

class moving_avg():

    def __init__(self, ticker):
        ### refresh lists each time
        self.ticker_price = []
        self.current_time = []
        self.list_ma = []
        self.action = []
        self.change = []

        self.main(ticker)

    def round_prec(x):
        return round(x, config.prec_lvl)
    
    def get_moving_average(self, x, k):
        df = pd.DataFrame(self.ticker_price)
        # exponential moving average
        moving_avg_ewm = df.ewm(k).mean().iloc[-1].values

        ## round moving average to nearest 5 dec
        rounded = moving_avg.round_prec(moving_avg_ewm[0])

        # add list of ma's
        self.list_ma.append(rounded)

        print(colored('MA: ' + str(rounded), 'blue'))

        if rounded > self.ticker_price[x]:
            self.action.append("BUY")
            print(colored("BUY", 'green'))
        elif rounded < self.ticker_price[x]:
            self.action.append("SELL")
            print(colored("SELL", 'red'))
        else:
            self.action.append("-----")
            print("-----")
    
    def get_price_and_price(self, x, df, k):
        # get time 
        t = time.localtime()
       
        # check if the dataframe is empty
        if df.empty:
            quit()

        lastPrice_historical = df['mean']


        pct_change = []
        self.ticker_price.append(lastPrice_historical[x])

        self.current_time.append(time.strftime("%H:%M:%S", t))

        self.change.append((self.ticker_price[x] - self.ticker_price[x-1]))

        pct_change.append(self.change[x] / self.ticker_price[x-1])

        print('\n')
        if x == 0:
            return 0
        elif self.change[x] > 0:
            print('Price: ' + colored(str(moving_avg.round_prec(self.ticker_price[x])), 'green'))
            # print("\n    Change: ", colored(str(round(change[x], 6)), 'green'))
        elif self.change[x] < 0:
            print('Price: ' + colored(str(moving_avg.round_prec(self.ticker_price[x])), 'red'))
            # print("\n    Change: ", colored(str(round(change[x], 6)), 'red'))
        else: 
            print('Price: ' + colored(str(moving_avg.round_prec(self.ticker_price[x])), 'grey'))
            # print("\n    Change: ", colored(str(round(change[x], 6)), 'grey'))

        if x >= k:
            moving_avg.get_moving_average(self, x, k)

    def main(self, ticker):

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
            self.list_ma.append("")
        for i in range(k):
            self.action.append("")

        ### get price info 
        for x in range(iterations):
            moving_avg.get_price_and_price(self, x, df, k)
            # # since the system only evaluating the past no need for sleep function
            # time.sleep(0.0001)


        # add the lists to the data table for price, ma, and actions
        price_ma_actions = pd.DataFrame(columns=['Current Time', 'Price', 'Moving Average', 'Action'])
        price_ma_actions['Current Time'] = self.current_time
        price_ma_actions['Price'] = self.ticker_price
        price_ma_actions['Moving Average'] = self.list_ma
        price_ma_actions['Action'] = self.action


        # save file to folder and filename
        price_ma_actions.to_csv(os.path.join(csv_save_location, filename))

        evaluate.evaluate_performance(filename)

    
    

        

    
