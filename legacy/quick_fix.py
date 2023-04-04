import pandas as pd

df = pd.read_csv('overview/0.1-3233n01.csv')

df2 = pd.DataFrame()
df1 = pd.DataFrame()

df2['Ticker:'] = df['Ticker:']
df2['Total Gain:'] = df['Total Gain:']

df1['Trades:'] = df['Trades']

l = len(df1['Trades:'])

trades = []

for row in range(l):
    s = df1['Trades:'][row]
    s = s[5:]
    s = s[:2]
    trades.append(s)

df2['Trades:'] = trades

df2.to_csv('overview/adj0.1-3233n01.csv')