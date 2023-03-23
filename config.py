### global variables

version = '0.10'

# value of k for moving average
k = 3

# # legacy 
# # window of evaluation (i.e. how many data points do we wait until it materializes)
# # eval_len = 3

# pre-market hours (default = True)
pre_mrkt = False

# post-market hours (default = True)
post_mrkt = False

# how precise we want our numbers
prec_lvl = 5

# where CSV's will be saved
csv_save_location = 'CSVs'

# where performance bottomlines are saved
performance_folder = 'Performance'

# where performance figures are saved
performance_figures_folder = 'Performance Figures'

# decide if we want recent data or use a .csv file with the data (default='current') other option is 'historical'
currency = 'current'

# date on which you want to analyze the stock, default='today'
# format: YYYY-MM-DD
data_date = '2023-03-22'

