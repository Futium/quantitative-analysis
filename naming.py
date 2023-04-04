import config
from datetime import date
from datetime import datetime

pre_mrkt = config.pre_mrkt
post_mrkt = config.post_mrkt
data_date = config.data_date.lower()
version = config.version

## convert to integer then to string   
pre_mrkt = str(int(config.pre_mrkt == True))
post_mrkt = str(int(config.post_mrkt == True))

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

# get date value
if data_date != 'today':
    file_date = datetime.strptime(data_date, '%Y-%m-%d').date()
else:
    file_date = date.today()


# convert them to single char 
file_dates = [str(file_date.year)[2:], make_one_char(file_date.month), make_one_char(file_date.day)]

def filename(ticker, k):
    if k == 'raw':
        filename = ticker + '-' + version + '-' + ''.join(file_dates) + '.parquet'
    else: 
        # if the ticker is an actual stock
        if ticker != '':
            # [ticker]-[version]-[k][date][preMRKT][postMRKT].csv
            filename = ticker + '-' + version + '-' + str(k) + ''.join(file_dates) + pre_mrkt + post_mrkt + '.parquet'
        else: 
            filename = version + '-' + str(k) + ''.join(file_dates) + pre_mrkt + post_mrkt + '.csv'
    
    return filename
