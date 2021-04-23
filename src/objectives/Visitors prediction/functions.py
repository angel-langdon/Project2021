# %%
import os
from datetime import timedelta

import holidays
import numpy as np
import pandas as pd
from utils.date_utils.date_formats import DATE_FORMATS
from utils.download_data import data_dtypes as dtypes
from utils.path_utils import paths

from visitors_prediction import (add_last_visits, drop_duplicate_stores,
                                 explode_vists_by_day, filter_selected_cols,
                                 read_patterns_data)

#%%
df = read_patterns_data('/Users/mazcu/Projects/Project2021/src/datasets/processed/Houston/subway.csv')
df = drop_duplicate_stores
df = explode_vists_by_day(df_original)
df = filter_selected_cols(df)
df = add_last_visits(df)
#%%
def is_weekend(df):
    df = df.copy()
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
    df.copy()
    holi = holidays.CountryHoliday('US', prov="Houston", state='TX')
    df["is_holiday"] = [1 if d in holi else 0 for d in df["date"]]
    return df


def add_last_visits(df: pd.DataFrame):
    df = df.copy()
    dict_last_visits = {"yesterday": timedelta(days=1),
                        "last_week": timedelta(days=7)}
    suffix = "_visits"
    for period, diff in dict_last_visits.items():
        df[period] = df["date"] - diff
        df[period+suffix] = 0

    for placekey in df["placekey"].unique():
        for period in dict_last_visits:
            is_store = df["placekey"] == placekey
            is_period = df["date"] == period

            peroid_vists_col = (is_store) & (is_period)
            df.loc[is_store, period+suffix] = df.loc[peroid_vists_col, "visits"]
    return df


# %%
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
    # cosa = cosa[['census_block_group', 'B19013e1']]

    new['cbg_income'] = [0]*91824
    for row in cosa.iterrows():
        new['cbg_income'] = np.where(new['poi_cbg'] == str(
            row[1][0]), row[1][1], new['cbg_income'])

    return new


def rain(df):
    rain_2020 = pd.read_csv('data/rain_houston_2020.csv', sep=';')
    rain_2021 = pd.read_csv('data/rain_houston_2021.csv', sep=';')
    # df['date'] = df['date'].map(int)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    df['rain'] = [0]*91824
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
    df['cbg_population'] = [0]*91824
    for row in dat.iterrows():
        df['cbg_population'] = np.where(df['poi_cbg'].map(str) == str(
            int(row[1][0])), row[1][1], df['cbg_population'])
    return df


"""
EXECUTION MODE

subway = pd.read_csv('Subway_Houston_days.csv', encoding="utf-8") #Needed to filter by state TX.
subway = is_weekend(subway)
subway = is_holiday(subway)
subway = last_day_n_week(subway)
subway = income(subway)
subway = rain(subway)
subway = population(subway)
"""

"NEEDED THE PATH OF THE POPULATION.CSV, DEVICES.CSV, SUBWAY_HOUSTON_DAYS (SUBWAY)"

def get_population(df):
    dat = pd.read_csv('/Users/mazcu/Downloads/population.csv')
    dat['poi_cbg'] = dat['poi_cbg'].astype(int).astype(str)
    df = df.merge(nf, on='poi_cbg', how='left')
    return df
        
def get_devices(df):
    nf = pd.read_csv('/Users/mazcu/Downloads/devices.csv') #home_panel_summary
    nf['poi_cbg'] = nf['poi_cbg'].astype(int).astype(str)
    df['poi_cbg'].astype(int).astype(str)
    print(type(df['poi_cbg']), type(nf['poi_cbg']))
    df = df.merge(nf, on='poi_cbg', how='left')
    
    return df

def get_real_visits(df):
    df['real_visits'] = (df['population'] // df['devices'])*df['visits']
    return df








