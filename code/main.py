import sys

import numpy as np
import pandas as pd
import matplotlib as plt

air_df = pd.read_csv('APIMS-final.csv')
air_df['Time'] = pd.to_datetime(air_df.Time)
air_df['year'] = pd.DatetimeIndex(air_df.Time).year
air_df['month'] = pd.DatetimeIndex(air_df.Time).month
air_df['day'] = pd.DatetimeIndex(air_df.Time).day
test=pd.DataFrame()

#To extract data from 2018 to 2022
for x in range(2018,2023,+1):
    air_want_df=air_df.loc[air_df.year==x]
    test=pd.concat([test,air_want_df])
test.reset_index(drop=True,inplace=True)
test.drop('Muar', axis=1, inplace=True)

null_values = test.isnull()
#fill in null values:
for col in test.columns:
    test[col].fillna(method='bfill', limit=90, inplace=True)

for col in test.columns:
    test[col].fillna(method='ffill', limit=90, inplace=True)

for col in test.columns:
    if col!='Time' and col != 'year' and col != 'day' and col != 'month':  # Skip the 'Year', 'Day', and 'Month' columns
        for year in test['year'].unique():
            mean_api = test.loc[(test['year'] == year), col].mean()
            # Replace missing values with the mean API
            test[col].fillna(mean_api,inplace=True)

print(test)
missing=test.isnull().sum()
missing_per=100*(missing/len('Time'))
print(type(missing_per))
print(missing_per.sort_values(ascending=False))

test.to_csv('cleaned_air_data.csv',index=False)