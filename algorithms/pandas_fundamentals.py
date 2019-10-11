import pandas as pd
import os
import numpy as np

PF_ROOT = "C:\\Users\\David\\dev\\toy-algorithms"
COLLECTION_ROOT = os.path.join(PF_ROOT, "pandas-fundamentals\\demos\\collection-master")

CSV_PATH = os.path.join(COLLECTION_ROOT, "artwork_data.csv")
COLS_TO_USE = ['id', 'artist', 'title', 'medium', 'year', 'acquisitionYear', 'height', 'width', 'units']

# Read in artwork data-frame
df = pd.read_csv(CSV_PATH, usecols=COLS_TO_USE, index_col='id')

# Pickle data-frame to save and reload.
PICKLE_FILE = os.path.join(COLLECTION_ROOT, "artwork_data_frame.pickle")
df.to_pickle(PICKLE_FILE)

print(df.head())

s = (df['artist'] == 'Bacon, Francis')
print(s.value_counts())

artist_counts = df['artist'].value_counts()
print("\nNumber or art works created by Francis Bacon = {}".format(artist_counts['Bacon, Francis']))

# Confirm can read pickled file
df1 = pd.read_pickle(PICKLE_FILE)
assert(df.shape == df1.shape)

## loc() vs. iloc()

# confirm we get an array of ints when using np.where()
foob = np.where(df1['artist'].str.contains('Robert'))

# Integer indexers only work with the iloc() method.
df_sub = df1.iloc[np.where(df1['artist'].str.contains('Robert'))]

# Boolean indexers only work with the 'loc()' method.
df_suba = df1.loc[df1['artist'] == 'Bacon, Francis', :]

# Also, using column and row names works with loc().
print(df.loc[1035, 'artist'])

print(df.iloc[0, 0])
print('\n')

print(df.iloc[0, :].head())
print('\n')

print(df.loc[:, 'artist'].head())  # uses 'artist' ==> loc

print(df.iloc[:, 0].head())  # uses int value of column ==> iloc

## Coercing input data

# Will switch to df1, which is the one red in after being pickled
pd.to_numeric(df1['width'], errors='coerce')

df1.loc[:, 'width'] = pd.to_numeric(df1['width'], errors='coerce')
df1.loc[:, 'height'] = pd.to_numeric(df1['height'], errors='coerce')

df1['area'] = df1['height'] * df1['width']

# Get artwork with the largest area.
max_area = df1['area'].max()
print(max_area)
ixm = df1['area'].idxmax()
print(df1.loc[ixm])

types = (df1['medium'].unique().shape[0])
print("Number of types is {}".format(types))  # ==> implies 3414 !!

# What is want to limit it to painting, or oil paintings.
locs_ = np.where(np.logical_and(df1['medium'].str.contains('paint'),
                                df1['medium'].str.contains('canvas')))
df1_paint = df1.iloc[locs_]

type_list = df1_paint['medium'].unique()
types = type_list.shape[0]
print("Number of types is {}".format(types))  # ==> implies 3414 !!

# Get max of more limited selection of paintings on canvas.
max_area = df1_paint['area'].max()
print(max_area)
ixm = df1_paint['area'].idxmax()
print(df1_paint.loc[ixm])

dfgb = df1.groupby('artist')

print('\n')
#print(dfgb.head())

small_df = df1.iloc[49980:50019, :].copy()
grouped = small_df.groupby('artist')

print("typed grouped = {}".format(type(grouped)))

for name, group_df in grouped:
    print("\n{}, acquired {}".format(name, group_df['acquisitionYear'].min()))

# Next two functions will illustrate
# how one could use groupby and looping to fill values
# based on the subgroup. More efficient techniques
# will be illustrated later.
foo_df = small_df.copy()

pd.to_numeric(foo_df['height'], errors='coerce')
foo_df.at[4708, 'height'] = 155.
foo_df.at[[4704,11838,16435], 'height'] = np.NaN

def fill_values_most_frequent(series):
    values_counted = series.value_counts()
    if values_counted.empty:
        return series
    most_frequent = values_counted.index[0]
    new_series = series.fillna(most_frequent)
    return new_series

def fill_by_artist(source_df):
    new_group_dfs = []
    for name, group_df in source_df.groupby('artist'):
        artist_df = group_df.copy()
        artist_df.loc[:, 'height'] = fill_values_most_frequent(group_df['height'])
        new_group_dfs.append(artist_df)
    new_df = pd.concat(new_group_dfs)
    return new_df

filled_df = fill_by_artist(foo_df)

# OR more simply, do the following...
grouped_height = foo_df.groupby('artist')['height']
# Transform takes a function, in this case our fill_values... function.
foo_df.loc[:, 'height'] = grouped_height.transform(fill_values_most_frequent)

# The quick way to find all the minimum years of acquisition is as follows:
grouped_by_acquisition_year = small_df.groupby('artist')['acquisitionYear']
min_acquisition_years = grouped_by_acquisition_year.agg(np.min)
# or just, min_acquisition_years = grouped_by_acquisition_year.min()
print('\n', min_acquisition_years)

# Other quick techniques using groupby
# 1. Get only those titles that appear more than once for each artist.
grouped_by_title = small_df.groupby('title')
condition = lambda x: len(x.index) > 1
filtered_df = grouped_by_title.filter(condition)
print('')
print(filtered_df['title'].unique())

x = 1