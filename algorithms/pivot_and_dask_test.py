import pandas as pd
import dask
import dask.dataframe as dd
import numpy as np
import time


# Target dataframe after pivot
columns = ['MSFT', 'IBM', 'AAPL', 'GOOG', 'AMZN', 'BRKB']
start_prices = np.array([144.0, 138.0, 257., 1292.0, 1724., 221.0])

start_prices -= 0.5

shape_ = 10000 # 100
time_arr = np.zeros(shape_)
price_arr = np.zeros(shape_)
symbol_arr = np.empty(shape_, dtype=np.object)
data_frame_list = []
for (idx, symbol) in enumerate(columns):
    for i in range(shape_):
        time_arr[i] = float(i+1)
        price_arr[i] = start_prices[idx] + np.random.random()
        symbol_arr[i] = symbol

    df = pd.DataFrame()
    df['time'] = time_arr
    df['price'] = price_arr
    df['symbol'] = symbol_arr

    data_frame_list.append(df)


# pandas
start = time.time()

df0 = pd.concat(data_frame_list)
df0.sort_values(by='time', inplace=True)
df1 = df0.pivot(index='time', columns='symbol', values='price')
df1.reset_index(inplace=True)

end = time.time()

print(f"Total for pandas = {end-start}")
print(f"column names in data frame, {df1.columns}")

# dask
'''
# Nevermind...
# From the Dask documentation:
# Note that, despite parallelism, Dask.dataframe may not always be faster than Pandas.
# We recommend that you stay with Pandas for as long as possible before switching to Dask.dataframe.

start1 = time.time()
df0 = dd.concat(data_frame_list)
df0.compute()
df0a = df0.set_index('time', sorted=True)
df0a.compute()
df1 = df0a.pivot(index='time', columns='symbol', values='price')
df1.reset_index(inplace=True)
df1.compute()
end1 = time.time()
print("Total for pandas = {end1-start1}")
print(f"column names in data frame, {df1.columns}")
'''

x = 1


