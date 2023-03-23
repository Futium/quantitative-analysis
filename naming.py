import config
from datetime import date
from datetime import datetime
import math

k = str(config.k)
pre_mrkt = config.pre_mrkt
post_mrkt = config.post_mrkt
data_date = config.data_date.lower()
version = config.version

## convert to integer then to string   
pre_mrkt = str(int(config.pre_mrkt == True))
post_mrkt = str(int(config.post_mrkt == True))


# get date value
if data_date != 'today':
    file_date = datetime.strptime(data_date, '%Y-%m-%d').date()
else:
    file_date = date.today()

def make_one_char(x):
    list = [
        '0', 
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        'a',
        'b',
        'c',
        'd',
        'e',
        'f',
        'g',
        'h',
        'i',
        'j',
        'k',
        'l',
        'm',
        'n',
        'o',
        'p',
        'q',
        'r',
        's',
        't',
        'u',
        'v',
        'w',
        'x',
        'y',
        'z'
    ]

    return list[x]

# convert them to single char 
file_dates = [str(file_date.year)[2:], make_one_char(file_date.month), make_one_char(file_date.day)]

def filename(ticker):
    # [version]-[k][date][preMRKT][postMRKT].csv
    filename = ticker + '-' + version + '-' + k + ''.join(file_dates) + pre_mrkt + post_mrkt + '.csv'

    return filename
