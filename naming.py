import config
import futium
from datetime import date
from datetime import datetime

pre_mrkt, post_mrkt, data_date, version = config.pre_mrkt, config.post_mrkt, config.data_date.lower(), config.version

## convert to integer then to string   
pre_mrkt, post_mrkt = str(int(config.pre_mrkt == True)), str(int(config.post_mrkt == True))

# get date value
if data_date != 'today':
    file_date = datetime.strptime(data_date, '%Y-%m-%d').date()
else:
    file_date = date.today()


# convert them to single char 
file_dates = [str(file_date.year)[2:], futium.oneChar(file_date.month), futium.oneChar(file_date.day)]

def filename(ticker, k):
    if k == 'raw':
        filename = "".join([ticker, '-', ''.join(file_dates), '.parquet'])
    else: 
        # if the ticker is an actual stock
        if ticker != '':
            # [ticker]-[version]-[k][date][preMRKT][postMRKT].csv
            filename = "".join([ticker, '-', version, '-', str(k), ''.join(file_dates), pre_mrkt, post_mrkt, '.parquet'])
        else: 
            filename = "".join([version, '-' + str(k), ''.join(file_dates), pre_mrkt, post_mrkt, '.csv'])
    
    return filename
