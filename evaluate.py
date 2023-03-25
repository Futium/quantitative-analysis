import config
import pandas as pd
import os

csv_save_location = config.csv_save_location
performance_folder = config.performance_folder
performance_figures_folder = config.performance_figures_folder


def evaluate_performance(filename):
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

    # number of trades
    num_of_trades = len(list_of_dfs)

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
    total_gain = sum(pct_gain)
    ttl_gain_string = str(total_gain) + '%'

    ### take the performance and get them into a .csv file
    # find the performance and make them into a table
    performance_values = [[ttl_gain_string, num_of_trades]]
    performance = pd.DataFrame(performance_values, columns=['Total Gain:', 'Number of Trades'])

    # create file name for performance
    performance_file_name = 'performance-for-' + filename

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
    performance_figures_file_name = 'performance-figures-'+ filename

    # save to csv
    data.to_csv(os.path.join(performance_figures_folder, performance_figures_file_name))
