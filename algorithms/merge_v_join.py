import pandas as pd

df1 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]},
                   index = [2001, 2002, 2003, 2004])

df2 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Int_rate':[2, 3, 2, 2],
                    'US_GDP_Thousands':[50, 55, 65, 55]},
                   index = [2004, 2005, 2006, 2007])

df3 = pd.DataFrame({'HPI':[80,85,88,85],
                    'Unemployment':[7, 8, 9, 6],
                    'Low_tier_HPI':[50, 52, 50, 53]},
                   index = [2001, 2002, 2003, 2004])

# Add all rows of two dataframes together, sort, and take the last one based on index
dfm2 = df2.append(df1)
print("\n", len(dfm2))
dfm2.sort_index(inplace=True)
dfm2['index1'] = dfm2.index
print(dfm2)
dfm2.drop_duplicates(subset='index1', keep='first', inplace=True)
dfm2.drop('index1', axis=1, inplace=True)
print("\n", dfm2)
