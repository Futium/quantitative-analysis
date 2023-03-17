import yfinance as yf
import pandas as pd

ticker = input("What Ticker are you seeking analysis on?\n").upper()

data = yf.download(ticker, period='1d', interval='1m', prepost=True)

df = pd.DataFrame(data)

df.index = df.index.astype(str)

# drop all rows that include 4 AM, 5AM, 6AM, 7AM, 8AM, I'm not gonna be up at that time
df = df[df.index.str.contains(" 04:") == False]
df = df[df.index.str.contains(" 05:") == False]
df = df[df.index.str.contains(" 06:") == False]
df = df[df.index.str.contains(" 07:") == False]
df = df[df.index.str.contains(" 08:") == False]
df = df[df.index.str.contains(" 09:0") == False]
df = df[df.index.str.contains(" 09:1") == False]
df = df[df.index.str.contains(" 09:2") == False]

df['mean'] = df.iloc[:, 1:5].mean(axis=1)

i = 0

moving_avg = []

window_size = 10

arr = df['mean']

while i < len(arr) - window_size + 1:
    # Store elements from i to i+window_size
    # in list to get the current window
    window = arr[i : i + window_size]
  
    # Calculate the average of current window
    window_average = round(sum(window) / window_size, 2)
      
    # Store the average of current
    # window in moving average list
    moving_avg.append(window_average)
      
    # Shift window to right by one position
    i += 1

print(moving_avg)

# df.to_csv(ticker + '.csv')

