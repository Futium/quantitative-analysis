### global variables

# value of k for moving average
k = 3

# window of evaluation (i.e. how many data points do we wait until it materializes)
eval_len = 3

# how precise we want our numbers
prec_lvl = 5

# where CSV's will be saved
csv_save_location = 'CSVs'

# where performance bottomlines are saved
performance_folder = 'Performance'

# where performance figures are saved
performance_figures_folder = 'Performance Figures'

# decide if we want recent data or use a .csv file with the data (default='current') other option is 'historical'
currency = 'historical'

# date on which you want to analyze the stock, default='today'
# if the file with said date does not exist then an error will be logged.
data_date = '2023-03-21'