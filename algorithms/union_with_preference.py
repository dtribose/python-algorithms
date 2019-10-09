import pandas as pd
import numpy as np


def union_df(a_df, b_df):
    """ generate the union of a and b...

    with a preference for b (or 'a') when they have the same time column.

    Consider b_df as the set of updates for 'a'
    """

    a_df1 = a_df.copy()
    b_df1 = b_df.copy()

    # create a temporary array to keep track of status of b_df1 rows.
    append_array = np.ones((b_df1.shape[0]),dtype=np.int8)

    a1_time_series = a_df1['time']

    # Override same time elements
    for index, row in b_df1.iterrows():
        ix = np.searchsorted(a1_time_series, row['time'])
        if ix < len(a_df1) and a_df1.loc[ix, 'time'] == row['time']:
            a_df1.loc[ix] = row  # replace row.
            append_array[index] = 0

    # Use flag, append_array==1 to get a sub-array of b_df1 to append to a_df1. Return that.
    locs_ = np.where(append_array==1)
    c_df_ = a_df1.append(b_df1.loc[ locs_ ])
    c_df = c_df_.sort_values(["time"])
    c_df.reset_index(inplace=True)

    return c_df


if __name__ == "__main__":
    a_df = pd.DataFrame(data=[('MSFT', 22, 1570554342), ('IBM', 33, 1570554343), ('VJET', 44, 1570554345)],
                        columns=['stock', 'price', 'time'],)

    b_df = pd.DataFrame(data=[('MSFT', 24, 1570554342), ('QQQ', 99, 1570554340)],
                        columns=['stock', 'price', 'time'],)

    c_df = union_df(a_df, b_df)

    assert(c_df.shape[0] == 4)
    ref = pd.Series(['QQQ', 'MSFT', 'IBM', 'VJET'], name='stock')
    assert(np.all(c_df['stock'] == ref))

    print('\nAll tests passed')