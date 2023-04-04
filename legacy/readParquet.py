import pandas as pd
import os
import yahoo_fin.stock_info as si

# folder = "Performance"
# filename = "performance-for-A-0.1-2234301.parquet"

# df = pd.read_parquet(os.path.join(folder, filename))

# df.to_csv('temp.csv')


sp500 = si.tickers_sp500()

print(len(sp500))