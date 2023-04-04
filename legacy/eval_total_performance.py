import naming
import config
import pandas as pd
import os

performance_folder = config.performance_folder
performance = []
trades = []

def ttl_performance(tickers, k):
    performance = []
    trades = []
    for ticker in tickers:
        filename = 'performance-for-' + naming.filename(ticker, k)
        df = pd.read_parquet(os.path.join(performance_folder, filename))
        performance.append(df['Total Gain:'][0])
        trades.append(df['Number of Trades'][0])

    df2 = pd.DataFrame()

    df2['Ticker:'] = tickers
    df2['Total Gain:'] = performance
    df2['Trades:'] = trades

    # insert '' to get the filename less the ticker
    overview_filename = naming.filename('', k)

    df2.to_csv(os.path.join(config.overview_folder, overview_filename))
