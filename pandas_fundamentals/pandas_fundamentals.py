import pandas as pd
import os
import time

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rcParams
# matplotlib.use('qtagg')

### These original paths referenced directories on a Windows PC. ###
# PF_ROOT = "C:\\Users\\David\\dev\\toy-algorithms"
# COLLECTION_ROOT = os.path.join(PF_ROOT, "pandas-fundamentals\\demos\\collection-master")

PF_ROOT = "/home/dctodd/dev/python/toy-algorithms"
COLLECTION_ROOT = os.path.join(PF_ROOT, "pandas_fundamentals/collection_masters")

CSV_PATH = os.path.join(COLLECTION_ROOT, "artwork_data.csv")
COLS_TO_USE = ['id', 'artist', 'title', 'medium', 'year', 'acquisitionYear', 'height', 'width', 'units']


def ztest_pandas_fundamentals():

    # Read in artwork data-frame
    df = pd.read_csv(CSV_PATH, usecols=COLS_TO_USE, index_col='id')

    # Take a quick look at the data
    print(df.head())

    s = (df['artist'] == 'Bacon, Francis')
    print(s.value_counts())

    artist_counts = df['artist'].value_counts()
    print("\nNumber or art works created by Francis Bacon = {}".format(artist_counts['Bacon, Francis']))

    # Using column and row names works with loc().
    print("Using column and row names in loc:\n")
    print(df.loc[1035, 'artist'])
    print(df.loc[:, 'artist'].head())  # uses 'artist' ==> loc

    print("\nUsing only ints in iloc:\n")
    print(df.iloc[0, 0])
    print('\n')
    print(df.iloc[0, :].head())
    print('\n')
    print(df.iloc[:, 0].head())  # uses int value of column ==> iloc

    ## Coercing input data   # What is coercing?
    pd.to_numeric(df['width'], errors='coerce')

    df.loc[:, 'width'] = pd.to_numeric(df['width'], errors='coerce')
    df.loc[:, 'height'] = pd.to_numeric(df['height'], errors='coerce')

    df['area'] = df['height'] * df['width']

    # Get artwork with the largest area.
    max_area = df['area'].max()
    print(f"max area = {max_area}")
    ixm = df['area'].idxmax()
    print(f"Index with max area = {df.loc[ixm]}")

    types = (df['medium'].unique().shape[0])
    print("Number of types is {}".format(types))  # ==> implies 3414 !!

    # Limit it to painting, or oil paintings.
    locs_ = np.where(np.logical_and(df['medium'].str.contains('paint'),
                                    df['medium'].str.contains('canvas')))
    df_paint = df.iloc[locs_]
    type_list = df_paint['medium'].unique()
    types = type_list.shape[0]
    print("Number of types is {}".format(types))  # ==> implies 3414 !!

    # Get max of more limited selection of paintings on canvas.
    max_area = df_paint['area'].max()
    ixm = df_paint['area'].idxmax()
    print()
    print("Artist with the largest painting ({} mm**2) is {}".format(max_area, df_paint.loc[ixm, 'artist']))

    # Pickle data-frame to save and reload.
    pickle_file = os.path.join(COLLECTION_ROOT, "artwork_data_frame.pickle")
    df.to_pickle(pickle_file)

    return df, pickle_file

def ztesting_indexing(df):
    # Checking that we get an array of ints when using np.where()
    foo_bar_ints = np.where(df['artist'].str.contains('Robert'))
    df_sub0 = df.iloc[foo_bar_ints]

    # integer indexers only work in iloc?
    df_sub1 = df.iloc[np.where(df['artist'].str.contains('Robert'))]

    assert(df_sub0.shape == df_sub1.shape)  # These objects are different but have identical content.

    # Boolean indexers only work with the 'loc()' method.
    df_sub2 = df.loc[df['artist'] == 'Bacon, Francis', :]

    # Any detailed test here?
    x = 1

def ztest_unpickle_groupby(pickle_file, df):

    df1 = pd.read_pickle(pickle_file)

    # Confirm can un-pickled dataframe matches the original
    assert(df.shape == df1.shape)

    dfgb = df1.groupby('artist')

    print('\n')
    # print(dfgb.head())  # for testing

    small_df = df1.iloc[49980:50019, :].copy()
    grouped = small_df.groupby('artist')

    print("typed grouped = {}".format(type(grouped)))

    for name, group_df in grouped:
        print("\n{}, acquired {}".format(name, group_df['acquisitionYear'].min()))

    # Next two functions will illustrate how one could use groupby and looping to fill values
    # based on the subgroup. More efficient techniques will be illustrated later.
    foo_df = small_df.copy()

    pd.to_numeric(foo_df['height'], errors='coerce')
    foo_df.at[4708, 'height'] = 155.
    foo_df.loc[[4704, 11838, 16435], 'height'] = np.NaN

    x = 1

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
    duped_titles = grouped_by_title.filter(lambda x: len(x.index) > 1)
    print('')
    print(duped_titles['title'].unique())

    # now do this for all of df1
    grouped_by_title = df1.groupby('title')
    title_count = grouped_by_title.size().sort_values(ascending=False)
    print(title_count)

    duped_titles = grouped_by_title.filter(lambda x: len(x.index) > 1)
    print('\nDuped Titles:')
    print(duped_titles['title'])

    dt_cp = duped_titles.copy()
    print(dt_cp['title'])

    dt_cp.sort_values('title', inplace=True)
    print('\nDuped Titles sorted:')
    print(dt_cp['title'])

    # Look at all art work for the smallest height by artist.
    print()
    min_height = df1.groupby('artist')['height'].agg(np.min)
    print(min_height)
    # 'van Elk, Ger' is the last one at 1000.0

    van_elk_array = np.where(df1['artist'].str.contains('van Elk, Ger'))
    veg_df1 = df1.iloc[van_elk_array]


    sm_excel_p2f = os.path.join(PF_ROOT, "small_no_index.xlsx")
    small_df.to_excel(sm_excel_p2f, index=False, columns=['artist', 'title', 'year'])

    multiple_p2f = os.path.join(PF_ROOT, "multiple_sheets.xlsx")

    with pd.ExcelWriter(multiple_p2f) as writer:
        small_df.to_excel(writer, sheet_name='Preview', index=False)
        df1.to_excel(writer, sheet_name="Complete", index=False)

    '''
    # already exists. See how to update.
    artist_db = os.path.join(PF_ROOT, 'artist.db')
    with sqlite3.connect(artist_db) as conn:
        small_df.to_sql('SmallSet', conn)
    '''

    # @@@ implement postgres on my system
    # with sa.create_engine('postgresql://localhost/my_data') as conn:
    #    small_df.to_sql('SmallSet, conn')

    small_json_p2f = os.path.join(PF_ROOT, 'small_df.json')
    small_df.to_json(small_json_p2f, orient='table')


def ztest_plotting(df):
    ## Plotting

    title_font = {'family': 'source sans pro',
                  'color': 'darkblue',
                  'weight': 'normal',
                  'size': 20,
                  }
    labels_font = {'family': 'consolas',
                   'color': 'darkred',
                   'weight': 'normal',
                   'size': 16,
                   }

    acquisition_years = df.groupby('acquisitionYear').size()
    #acquisition_years.plot()
    #plt.show()

    rcParams.update({'figure.autolayout': True,
                     'axes.titlepad': 20})
    fig = plt.figure()
    subplot = fig.add_subplot(1, 1, 1)
    acquisition_years.plot(ax=subplot, rot=45, logy=True, grid=True)
    subplot.set_xlabel("Acquisition Year", labelpad=10)  #, fontdict=labels_font)
    subplot.set_ylabel("Artworks Acquired")  #, fontdict=labels_font)
    subplot.set_title("Tate Gallery Acquisitions")  #, fontdict=title_font)
    subplot.locator_params(nbins=40, axis='x')

    fig.show()

    time.sleep(10)

    fig.savefig(os.path.join(PF_ROOT, 'plot.png'))
    fig.savefig(os.path.join(PF_ROOT, 'plot.svg'), format='svg')


if __name__ == "__main__":

    df_, pickle_file_ = ztest_pandas_fundamentals()

    ztesting_indexing(df_)

    ztest_unpickle_groupby(pickle_file_, df_)

    ztest_plotting(df_)
