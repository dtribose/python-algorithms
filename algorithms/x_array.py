import xarray as xr
import numpy as np
import pandas as pd

# todo: What difference between rand() versus random()
data = np.random.random((6,3)) * 1e5

locs = ['CA', 'OR', 'WA']

times = pd.date_range('2019-01-01', periods=6)

arr = xr.DataArray(data, coords=[times, locs],
                   dims=['time', 'state'],
                   name='Monthly State Income',
                   attrs={
                       'notes': ['Easter in late March'],
                       'release': 'First Release',
                       'source': 'US office of income',
                       'exclusions': ['Non taxable items brought forth from previous tax year'],
                   })

print(arr)