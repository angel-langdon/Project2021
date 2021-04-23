import json
import os
from datetime import datetime, timedelta

import holidays
import numpy as np
import pandas as pd

# df filtered by houston, needed to filter by state = TX (NOT IMPLEMENTED)

subway = pd.read_csv(
    '/Users/mazcu/Downloads/Subway_Houston_days.csv', encoding="utf-8")


def is_weekend(df):
    df['date'] = pd.to_datetime(df['date'])

    df['is_weekend'] = df['date'].dt.day_name()
    df.loc[df['is_weekend'] == "Saturday", 'is_weekend'] = 1
    df.loc[df['is_weekend'] == "Sunday", 'is_weekend'] = 1
    df.loc[df['is_weekend'] == "Monday", 'is_weekend'] = 0
    df.loc[df['is_weekend'] == "Tuesday", 'is_weekend'] = 0
    df.loc[df['is_weekend'] == "Wednesday", 'is_weekend'] = 0
    df.loc[df['is_weekend'] == "Thursday", 'is_weekend'] = 0
    df.loc[df['is_weekend'] == "Friday", 'is_weekend'] = 0

    return df


def is_holiday(df):
    holi = holidays.CountryHoliday('US', prov="Houston", state='TX')
    df["is_holiday"] = [1 if d in holi else 0 for d in df["date"]]
    return df


def last_day_n_week(df):
    stores = set(df['placekey'])
    i = 0
    for store in stores:
        new = df[df['placekey'] == store]
        l = []
        l_week = []
        # for row in new.iterrows():
        yesterday = new['date'] - timedelta(days=1)
        yesterday = yesterday.dt.strftime('%Y-%m-%d')

        week = new['date'] - timedelta(days=7)
        week = week.dt.strftime('%Y-%m-%d')

        set_raro = set(new['date'].dt.strftime('%Y-%m-%d'))
        for day, other in zip(yesterday, week):
            if day in set_raro:
                visits = list(new[new['date'] == day]['visits'])
                l.append(visits[0])

            else:
                l.append(0)

            if other in set_raro:
                vis = list(new[new['date'] == other]['visits'])
                l_week.append(vis[0])
            else:
                l_week.append(0)

        new['visits_last_day'] = l
        new['visits_last_week'] = l_week

        if i == 0:
            old = new
            i += 1
        else:
            old = pd.concat([old, new])
    return old


def income(df):

    cosa = pd.read_csv('data/income.csv', encoding="utf-8",
                       dtype={"census_block_group": "category"})

    df['poi_cbg'] = df['poi_cbg'].map(int)
    df['poi_cbg'] = df['poi_cbg'].map(str)

    new = df[df['region'] == 'TX']
    cbgs = set(new['poi_cbg'])

    cosa = cosa[cosa['census_block_group'].isin(cbgs)]
    #cosa = cosa[['census_block_group', 'B19013e1']]

    new['cbg_income'] = 0
    for row in cosa.iterrows():
        new['cbg_income'] = np.where(new['poi_cbg'] == str(
            row[1][0]), row[1][1], new['cbg_income'])

    return new


def rain(df):
    rain_2020 = pd.read_csv('data/rain_houston_2020.csv', sep=';')
    rain_2021 = pd.read_csv('data/rain_houston_2021.csv', sep=';')
    #df['date'] = df['date'].map(int)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    df['rain'] = 0
    l = [rain_2020, rain_2021]
    for rain_df in l:
        for row in rain_df.iterrows():
            df['rain'] = np.where(df['date'] == str(
                row[1][0]), row[1][1], df['rain'])

    return df


def population(df):
    dat = pd.read_csv('data/population.csv')
    cbgs = set(df['poi_cbg'])
    dat = dat[dat['census_block_group'].map(str).isin(cbgs)]
    dat = dat[['census_block_group', 'B00001e1']]
    df['cbg_population'] = 0
    for row in dat.iterrows():
        df['cbg_population'] = np.where(df['poi_cbg'].map(str) == str(
            int(row[1][0])), row[1][1], df['cbg_population'])
    return df


"""
df = df.merge(rain, on='date', how='left')


RUN EVERY FUNCTION (NOT UPDATED, THE PERFECT ONES ARE IN FUNCTIONS.PY)

subway = is_weekend(subway)
subway = is_holiday(subway)
subway = last_day_n_week(subway)
subway = income(subway)
subway = rain(subway)
subway = population(subway)

subway
"""

"""

FUNCTION 2 KNOW IN WHICH CBG FILE IS THE VARIABLE WE WANTED TO OBTAIN

import os

for filename in os.listdir('/Users/mazcu/Downloads/safegraph_open_census_data/data/'): 
    print(filename)
    cosa = pd.read_csv('/Users/mazcu/Downloads/safegraph_open_census_data/data/'+filename, encoding="utf-8")
    try:
        print(filename, cosa['B19013e1'])
    except:
        pass
        
OTHER TEST 4 OTHER VAR
    
for csv in os.listdir('/Users/mazcu/Downloads/safegraph_open_census_data/data/'):
    test = pd.read_csv(
        '/Users/mazcu/Downloads/safegraph_open_census_data/data/cbg_b00.csv' + csv)
    try:
        print(csv, test['B00001e1'])
    except:
        print(csv, 'NO')

"""

cbgs = set(subway['poi_cbg'])

# GETTING THE INCOME PER CBG
cosa = pd.read_csv('/Users/mazcu/Downloads/safegraph_open_census_data/data/cbg_b19.csv',
                   encoding="utf-8", dtype={"census_block_group": "category"})
cosa = cosa[cosa['census_block_group'].isin(cbgs)]
cosa = cosa[['census_block_group', 'B19013e1']]
cosa.to_csv('income.csv', index=False)

# GETTING THE POPULATION PER CBG
dat = pd.read_csv(
    '/Users/mazcu/Downloads/safegraph_open_census_data/data/cbg_b01.csv')
dat = dat[dat['census_block_group'].map(str).isin(cbgs)]
dat = dat[['census_block_group', 'B01001e1']]
dat.to_csv('population.csv', index=False)

# GETTING THE DEVICES PER CBG
# esto me lo pasó el nacho, balones a él
nf = pd.read_csv('/Users/mazcu/Downloads/home_panel_summary (3).csv')
nf = nf[nf['census_block_group'].map(str).isin(cbgs)]
nf = nf[['census_block_group', 'number_devices_residing']]
nf.to_csv('devices.csv', index=False)

# FORMULA 4 THE VISITS
subway['real_visits'] = (subway['cbg_population'] //
                         subway['cbg_devices'])*subway['visits']  # to avoid floats
