# %%
import json
import os
from collections import Counter
from datetime import datetime, timedelta

import holidays
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import xgboost as xgb
from sklearn import svm
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import (BayesianRidge, ElasticNet, HuberRegressor,
                                  Lasso, LinearRegression, Ridge)
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import (GridSearchCV, RandomizedSearchCV,
                                     train_test_split)
from sklearn.svm import SVR
from utils.date_utils.date_formats import DATE_FORMATS
from utils.download_data import data_dtypes as dtypes
from utils.download_data import datasets, download_safegraph_data
from utils.path_utils import paths

#from xgboost import XGBRegressor


def get_important_brands(df: pd.DataFrame):
    dic = Counter(df["brands"])
    dic = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True))
    brands = pd.DataFrame(dic.items(), columns=["brand", "count"])
    return brands.dropna()


def drop_duplicate_stores(patterns: pd.DataFrame):
    """ Drops duplicated rows of patterns data
    """
    df = patterns.copy()
    # We sort the data frame by placekey, date and latitude
    # to later drop the duplicates and keep the observations
    # that contain latitude and longitude values
    df = df.sort_values(by=["placekey",
                            "date_range_start",
                            "latitude"])
    df = df.drop_duplicates(subset=["placekey",
                                    "date_range_start",
                                    "date_range_end"],
                            keep="first")
    return df


def read_patterns_data(city, state, brand):
    path = paths.get_processed_file_path(state, city, brand+'.csv')
    if os.path.isfile(path):
        df = pd.read_csv(path, encoding="utf-8",
                         dtype=dtypes.mobility_dtypes)
        df = df.dropna(subset=["poi_cbg"])
        df["poi_cbg"] = df["poi_cbg"].astype("float64").astype("int64").astype("category")
        df = drop_duplicate_stores(df)
    else:
        msg = "Patterns data not found, should be here:\n"+path
        raise(FileNotFoundError(msg))
    return df


def explode_visits_by_day(df_old):
    def get_dictionary_list_visits_day(visits_list):
        return [{"visits": visits, "day": day + 1}
                for day, visits in enumerate(visits_list)]
    df: pd.DataFrame = df_old.copy()
    df["visits_by_day"] = df["visits_by_day"].apply(json.loads)
    df["date"] = pd.to_datetime([d.split("T")[0] for d in df["date_range_start"]],
                                format=DATE_FORMATS.DAY)
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["visits_by_day"] = [get_dictionary_list_visits_day(l)
                           for l in df["visits_by_day"]]
    df = df.explode(column="visits_by_day")
    keys = df["visits_by_day"].iloc[0].keys()
    for key in keys:
        df[key] = [d[key] for d in df["visits_by_day"]]
    df["date"] = [f"{y}-{m}-{d}" for y, m, d in zip(df["year"],
                                                    df["month"],
                                                    df["day"])]
    df["date"] = pd.to_datetime(df["date"],
                                format=DATE_FORMATS.DAY)
    return df


def add_week_columns(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df["week_day"] = df["date"].dt.day_name()
    df['is_weekend'] = 0
    weekends_day = ["Saturday", "Sunday"]
    for day in weekends_day:
        df.loc[df['week_day'] == day, 'is_weekend'] = 1
    return df


def add_is_holiday(df, city, state, country):
    df = df.copy()
    holi = holidays.CountryHoliday(country, prov=city, state=state)
    df["is_holiday"] = [1 if d in holi else 0 for d in df["date"]]
    return df


def add_rain(df, city, state):
    path = paths.get_processed_file_path(state, city, 'rain.csv')
    if os.path.isfile(path):
        rain_df = pd.read_csv(path)
        rain_df['date'] = pd.to_datetime(rain_df['date'],
                                         format=DATE_FORMATS.DAY)
        return df.merge(rain_df, on='date', how='left')
    else:
        msg = "Rain data is missing it shoud be here: \n"+path
        raise(FileNotFoundError(msg))


def add_area(df, city, state):
    path = paths.get_processed_file_path(state, city, 'geometry.csv')
    if os.path.isfile(path):
        area_df = pd.read_csv(path)
        area_df['area_square_feet'] = area_df['area_square_feet']*0.092903
        area_df = area_df.rename(
            columns={"area_square_feet": "area_square_meters"})
        return df.merge(area_df, on='safegraph_place_id', how='left')
    else:
        msg = "Geometry data is missing it shoud be here: \n"+path
        raise(FileNotFoundError(msg))


def add_income(df, city="Houston", state='TX'):
    df = df.copy()
    df["poi_cbg"] = df["poi_cbg"].astype(int).astype(str)
    file_name = "income.csv"
    path = paths.get_processed_file_path(state, city, file_name)
    # In case the file exist
    if os.path.isfile(path):
        income = pd.read_csv(path, dtype=dtypes.census_dtypes,
                             encoding="utf-8")
        income = income.rename(columns={"census_block_group": "poi_cbg",
                                    'B19013e1': 'income'})
        income["poi_cbg"] = income["poi_cbg"].astype(int).astype(str)
        return df.merge(income, on='poi_cbg', how="left")

    # else: In case the file doesn't exist
    census_path = paths.get_census_file_path("cbg_b19.csv")
    download_safegraph_data.download_census_data_if_necessary()
    income = datasets.filter_census_df(census_path,
                                       ['census_block_group', 'B19013e1'],
                                       df["poi_cbg"].unique())
    # rename the cols for convenience
    income = income.rename(columns={"census_block_group": "poi_cbg",
                                    'B19013e1': 'income'})
    # save the dataframe to cache it for the next time
    income.to_csv(path, index=False, encoding="utf-8")
    return df.merge(income, on='poi_cbg', how='left')


def add_population(df, city, state):
    df = df.copy()
    file_name = 'population.csv'
    path = paths.get_processed_file_path(state, city, file_name)
    if os.path.isfile(path):
        pop = pd.read_csv(path)
        pop = pop.rename(columns={"census_block_group": "poi_cbg",
                                    'B01001e1': 'population'})
        pop['poi_cbg'] = pop['poi_cbg'].astype(int).astype(str)
        return df.merge(pop, on='poi_cbg', how='left')
    else:
        census_path = paths.get_census_file_path("cbg_b01.csv")
        pop_id = "B01001e1"
        cbgs = df["poi_cbg"].unique()
        download_safegraph_data.download_census_data_if_necessary()
        pop = datasets.filter_census_df(census_path,
                                        ["census_block_group", pop_id],
                                        cbgs)
        pop = pop.rename(columns={pop_id: 'population',
                                  "census_block_group": 'poi_cbg'})
        pop['poi_cbg'] = pop['poi_cbg'].astype(int).astype(str)
        pop.to_csv(path, index=False, encoding="utf-8")
        return df.merge(pop, on='poi_cbg', how="left")


def add_devices(df, city, state):
    df = df.copy()
    file_name = "devices.csv"
    path = paths.get_processed_file_path(state, city, file_name)
    if os.path.isfile(path):
        # home_panel_summary
        devices = pd.read_csv(path)
        devices = devices.rename(columns={"census_block_group": "poi_cbg"})
        devices['poi_cbg'] = devices['poi_cbg'].astype(int).astype(str)
        return df.merge(devices, on='poi_cbg', how='left')
    else:
        devices = datasets.get_lastest_home_pannel_summary(df["poi_cbg"])
        devices = devices.rename(columns={"census_block_group": "poi_cbg"})
        devices["poi_cbg"] = devices["poi_cbg"].astype(int).astype(str)
        devices.to_csv(path, index=False, encoding="utf-8")
        return df.merge(devices, on="poi_cbg", how="left")


def compute_real_visits(df):
    """ Apply visits micro-normalization to get real visits"""
    df = df.copy()
    devices_col = "number_devices_residing"
    df['visits'] = (((df['population'] / df[devices_col]) * df['visits'])
                    .round().astype(int))
    return df

def modelate_visits(df):
    df = df.copy()
    df = df[df['visits'] != 0]
    df = df[df.groupby('placekey')['placekey'].transform('size') > 200]
    df2fill = df[df['safegraph_place_id'] == 'this is only to get an empty df']
    for place in df['safegraph_place_id'].unique():
        df_per_store = df[df['safegraph_place_id'] == place]
        g = []
        for nrow in range(df_per_store.shape[0]):
            if nrow == 0:
                g.append((df_per_store.iloc[nrow]['visits'] + df_per_store.iloc[nrow+1]['visits'])/2)
            elif nrow == df_per_store.shape[0]-1:
                g.append((df_per_store.iloc[nrow]['visits'] + df_per_store.iloc[nrow-1]['visits'])/2)
            else:
                g.append((df_per_store.iloc[nrow-1]['visits'] + df_per_store.iloc[nrow]['visits'] + df_per_store.iloc[nrow+1]['visits'])/3)
        c = df_per_store['visits']
        df_per_store['visits'] = g
        df_per_store['old_visits'] = c
        df2fill = pd.concat([df2fill, df_per_store])
    
    return df2fill

def add_last_visits(df: pd.DataFrame):
    """ Adds new visits columns to patterns data
    Arguments:
        df : The patterns dataframe
    Returns:
        The same patterns dataframe with the visits
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df["placekey"] = df["placekey"].astype(str)
    # Define the data periods we want to add
    dict_last_visits = {"yesterday": -timedelta(days=1),
                        "last_week": -timedelta(days=7)}
    # Default suffix for new visits columns
    suffix = "_visits"
    # For each period
    for period, diff in dict_last_visits.items():
        # Auxiliar dataframe for left joining on place key and date
        period_df = pd.DataFrame()
        period_df["placekey"] = df["placekey"]
        # new visits column
        period_visits_col = period+suffix
        # create the new date column to merge
        period_df["date"] = df["date"] - diff
        # assign to the peroid visits col the visits
        period_df[period_visits_col] = df["visits"]
        df = pd.merge(df, period_df, how="left",
                      on=["placekey", "date"])
        # drop the column from the auxiliar dataframe in case
        # there are more date periods to add
        period_df = period_df.drop(columns=[period_visits_col])
    return df


def mean_n_days(test, n):
    test = test.copy()
    test['date'] = pd.to_datetime(test.date)
    idx = pd.date_range(test.date.min(), test.date.max(), freq='D')
    df_eee = test.pivot(index='date', values='visits',
                        columns='placekey').reindex(idx)
    # print(df_eee.iloc[0])
    df2 = (df_eee.shift().rolling(
        window=n, min_periods=1).mean().reset_index().drop_duplicates())
    # print(df2['index'])
    df3 = (pd.melt(df2, id_vars='index', value_name='visits').sort_values(
        ['index', 'placekey']).reset_index(drop=True))
    df3 = df3.rename(
        columns={'index': 'date', 'visits': f'mean_last_{n}_days'})
    test = test.merge(df3, on=['placekey', 'date'], how='left')
    return test


def add_dummies(df, drop_first=False):
    df = df.copy()
    df = pd.get_dummies(df, columns=["year"], drop_first=drop_first)
    df["month"] = df["date"].dt.month_name()
    df = pd.get_dummies(df, columns=["month"], drop_first=drop_first)
    df["day_aux"] = df["date"].dt.day_name()
    df = pd.get_dummies(df, columns=["day_aux"],
                        prefix="day", drop_first=drop_first)
    return df


def add_location(df):  # DONE, BUT NO CONTRIBUTION TO THE MODEL.
    path = paths.get_processed_file_path(state, city, 'location.csv')
    aaaa = pd.read_csv(path)
    aaaa = aaaa.rename(columns={"areas": "location"})
    df = df.merge(aaaa, on='latitude', how='left')
    return df


def test_new_dummies(df, drop_first=False):
    df = df.copy()
    df = pd.get_dummies(df, columns=["location"],
                        prefix="loc", drop_first=drop_first)

    return df


def filter_columns(df):
    df = df.copy()
    target_cols = ['placekey', 'safegraph_place_id', "brands", 'latitude',
                   'longitude', 'street_address', 'postal_code',
                   'poi_cbg', 'date', 'year', 'month',
                   'day', 'visits']
    return df[target_cols]


def clean_stores(df):
    # Get rid of COVID window
    df = df[df['date'] > datetime(year=2020, month=3, day=15)]
    # It makes no sense for the model trying to predict 0 visits
    # because 0 visits reflects that probably the store was closed
    df = df[df['visits'] != 0]
    # We delete the stores that have less than 200 observations
    df = df[df.groupby('placekey')['placekey'].transform('size') > 200]
    # It is important to fill the values that have 0 with NAs
    # to backfill them later, if we delete the values that are 0
    # then we will loss 14000 rows more
    df['yesterday_visits'] = df['yesterday_visits'].replace(0.0, np.NaN)
    df['last_week_visits'] = df['last_week_visits'].replace(0.0, np.NaN)
    # Implementation of correct fill na

    df = (df.sort_values(["placekey", "date"]).groupby(
        "placekey", as_index=False).bfill().ffill())

    return df

def apply_mean(df):
    
    df = df.copy()
    df = df.sort_values(["safegraph_place_id", "date"])
    road2means = df[['safegraph_place_id', 'visits']]
    listvisits = []
    means = road2means.groupby("safegraph_place_id", as_index=False).mean()
    for place in df['safegraph_place_id'].unique():
        place_df = df[df['safegraph_place_id'] == place]
        mean2apply = means[means['safegraph_place_id'] == place]['visits']
        vis = place_df['visits']/float(mean2apply)
        listvisits.append(vis)
        
    flat_list = [item for sublist in listvisits for item in sublist]
    df['visits'] = flat_list
    return df

def apply_log(df):
    df = df.copy()
    df['visits'] =  np.log(df['visits'].map(str).map(float))
    return df

def clean_log(df):
    df = df.copy()
    df = df[df['visits'] > 0]
    return df

def impute_outliers(df):
    df = df.copy()
    df2fill = df[df['safegraph_place_id'] == 'this is only to get an empty df']

    for place in df['safegraph_place_id'].unique():
        df_per_store = df[df['safegraph_place_id'] == place]
        upper = df_per_store.visits.quantile(.95)
        lower = df_per_store.visits.quantile(.05)
        df_per_store['visits'] = df_per_store['visits'].clip(upper=upper, lower=lower)
        df2fill = pd.concat([df2fill, df_per_store])
        
    return df2fill


def get_data_with_0_dashboard(df):
    df = df.copy()
    def add_last_visits_modified(df: pd.DataFrame):
        
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        df["safegraph_place_id"] = df["safegraph_place_id"].astype(str)
        # Define the data periods we want to add
        dict_last_visits = {"yesterday": -timedelta(days=1),
                            "last_week": -timedelta(days=7)}
        # Default suffix for new visits columns
        suffix = "_visits"
        # For each period
        for period, diff in dict_last_visits.items():
            # Auxiliar dataframe for left joining on place key and date
            period_df = pd.DataFrame()
            period_df["safegraph_place_id"] = df["safegraph_place_id"]
            # new visits column
            period_visits_col = period+suffix
            # create the new date column to merge
            period_df["date"] = df["date"] - diff
            # assign to the peroid visits col the visits
            period_df[period_visits_col] = df["visits"]
            df = pd.merge(df, period_df, how="left",
                        on=["safegraph_place_id", "date"])
            # drop the column from the auxiliar dataframe in case
            # there are more date periods to add
            period_df = period_df.drop(columns=[period_visits_col])
        return df

    def mean_n_days_modified(test, n):
        test = test.copy()
        test['date'] = pd.to_datetime(test.date)
        idx = pd.date_range(test.date.min(), test.date.max(), freq='D')
        df_eee = test.pivot(index='date', values='visits',
                            columns='safegraph_place_id').reindex(idx)
        # print(df_eee.iloc[0])
        df2 = (df_eee.shift().rolling(
            window=n, min_periods=1).mean().reset_index().drop_duplicates())
        # print(df2['index'])
        df3 = (pd.melt(df2, id_vars='index', value_name='visits').sort_values(
            ['index', 'safegraph_place_id']).reset_index(drop=True))
        df3 = df3.rename(
            columns={'index': 'date', 'visits': f'mean_last_{n}_days'})
        test = test.merge(df3, on=['safegraph_place_id', 'date'], how='left')
        return test

    df2fill = df[df['safegraph_place_id'] == 'this is only to get an empty df']
    df2fill = df2fill[['date', 'visits', 'old_visits']]
    
    for place in df['safegraph_place_id'].unique():
        
        a = df[df['safegraph_place_id'] == place]
        start = df['date'].min()
        end = df['date'].max()
        delta = end - start
        list_dates  = [start + timedelta(days=i) for i in range(delta.days + 1)]
        l_dates = pd.DataFrame({'date':list_dates})

        place = list(a['safegraph_place_id'])[0]
        brand = list(a['brands'])[0]
        lat = list(a['latitude'])[0]
        lon = list(a['longitude_x'])[0]
        street = list(a['street_address'])[0]
        postal = list(a['postal_code'])[0]
        cbg = list(a['poi_cbg'])[0]

        get_cols = ['date', 'visits', 'old_visits']
        c = a[get_cols]
        df_to_add = l_dates.merge(c, on='date', how='left')

        df_to_add['safegraph_place_id'] = place
        df_to_add['brands'] = brand
        df_to_add['latitude'] = lat
        df_to_add['longitude'] = lon
        df_to_add['street_address'] = street
        df_to_add['postal_code'] = postal
        df_to_add['poi_cbg'] = cbg

        df2fill = pd.concat([df2fill, df_to_add])
        
    

    df2fill["month"] = df2fill["date"].dt.month
    df2fill["year"] = df2fill["date"].dt.year
    df2fill["day"] = df2fill["date"].dt.day
    df2fill = add_week_columns(df2fill)
    df2fill = add_income(df2fill, city, state)
    df2fill = add_area(df2fill, city, state)
    df2fill = add_is_holiday(df2fill, city, state, country)
    df2fill = add_rain(df2fill, city, state)
    df2fill = add_population(df2fill, city, state)
    df2fill = add_last_visits_modified(df2fill)
    df2fill = add_location(df2fill)
    df2fill = mean_n_days_modified(df2fill, 7)
    df2fill = mean_n_days_modified(df2fill, 30)
    df2fill['visits'] = df2fill['visits'].replace(np.NaN, 0.0)
    df2fill['old_visits'] = df2fill['old_visits'].replace(np.NaN, 0.0)
    df2fill['last_week_visits'] = df2fill['last_week_visits'].replace(np.NaN, 0.0)
    df2fill['mean_last_30_days'] = df2fill['mean_last_30_days'].replace(np.NaN, 0.0)
    df2fill['mean_last_7_days'] = df2fill['mean_last_7_days'].replace(np.NaN, 0.0)
    df2fill = df2fill.reset_index()
    df2fill.drop('index', axis=1)
    return df2fill

def income_visits(df, brand):
    df = df.copy()
    
    if brand == 'subway':
        df['income_visits'] = round(df['visits'] * 9.5).astype(int)
        df['min_income_visits'] = round(df['min_visits'] * 9.5).astype(int)
        df['max_income_visits'] = round(df['max_visits'] * 9.5).astype(int)
        
    elif brand == 'Starbucks':
        df['income_visits'] = round(df['visits'] * 4.10).astype(int)
        df['min_income_visits'] = round(df['min_visits'] * 4.10).astype(int)
        df['max_income_visits'] = round(df['max_visits'] * 4.10).astype(int)
    
    elif brand == 'Walmart':
        df['income_visits'] = round(df['visits'] * 55).astype(int)
        df['min_income_visits'] = round(df['min_visits'] * 55).astype(int)
        df['max_income_visits'] = round(df['max_visits'] * 55).astype(int)
    
    elif brand == 'old_navy':
        df['income_visits'] = round(df['visits'] * 50).astype(int)
        df['min_income_visits'] = round(df['min_visits'] * 50).astype(int)
        df['max_income_visits'] = round(df['max_visits'] * 50).astype(int)
        
    return df

def workforce(df, brand):
    df = df.copy()
    if brand == 'subway':
        df['workforce'] = round((df['visits'] * 4)/150).astype(int)
        df['workforce'] = np.where((df.workforce < 4),4,df.workforce)
        
    elif brand == 'Starbucks':
        df['workforce'] = round((df['visits'] * 4)/210).astype(int)
        df['workforce'] = np.where((df.workforce < 4),4,df.workforce)
    
    elif brand == 'Walmart':
        df['workforce'] = round((df['visits'] * 50)/2000).astype(int)
        df['workforce'] = np.where((df.workforce < 50),50,df.workforce)
       
    elif brand == 'old_navy':
        df['workforce'] = round((df['visits'] * 5)/250).astype(int)
        df['workforce'] = np.where((df.workforce < 5),5,df.workforce) 
    
    return df


def IC_visits(df, mae):
    df = df.copy()
    
    mean_visits = df['visits'].mean()
    mae_new = ((df['visits'] * mae) / mean_visits)
    
    df['min_visits'] = round(df['visits'] - mae_new)
    df['max_visits'] = round(df['visits'] + mae_new)
    
    return df
# %%

country = "US"
city = "Houston"
state = "TX"
brand = "old_navy"
df_original = read_patterns_data(city, state, brand)
df = explode_visits_by_day(df_original)
df = filter_columns(df)
df = add_week_columns(df)
df = add_income(df, city, state)
df = add_area(df, city, state)
df = add_is_holiday(df, city, state, country)
df = add_rain(df, city, state)
df = add_population(df, city, state)
df = add_devices(df, city, state)
df = compute_real_visits(df)
df = modelate_visits(df)

# IF YOU WANT THE MEAN VERSION
#df = apply_mean(df)

#IF YOU WANT THE LOG VERSION
#df = apply_log(df)
#df = clean_log(df)

df = add_last_visits(df)
df = add_location(df)
df = mean_n_days(df, 3)
df = mean_n_days(df, 7)  # No more time 4 mean_week, now it's this :S
df = mean_n_days(df, 14)
df = mean_n_days(df, 21)
df = mean_n_days(df, 30)
df = mean_n_days(df, 60)

df = clean_stores(df)
df = impute_outliers(df)
df = test_new_dummies(df)
#df = add_dummies(df, drop_first=False)
# %%


def filter_model_columns(df: pd.DataFrame):
    exclude_cols = ['placekey', 'safegraph_place_id', 'brands', 'latitude', 'longitude', 'street_address', 'date',
                    'week_day', 'is_weekend', 'number_devices_residing', 'postal_code', 'poi_cbg',
                    'month', 'year']
    get_cols = ['day', 'rain', 'yesterday_visits', 'last_week_visits', 'mean_last_7_days', 'mean_last_30_days', 'visits', 'old_visits']  # include area_square_meters???
    cols = [col for col in df.columns if col in get_cols]
    return df[cols]


def get_correlation_plot(df):
    corr = df.corr().round(2)
    return corr.style.background_gradient(cmap='coolwarm')


def get_sorted_coefs(columns, coefficients):
    coefs = {col: coef for col, coef in zip(columns, coefficients)}
    coefs = dict(sorted(coefs.items(), key=lambda x: abs(x[1]), reverse=True))
    return coefs


# get_correlation_plot(df)

# %%
# DO YOU WANT THE DATA FOR THE DASHBOARD?
# IF YES, EXECUTE THE FOLLOWING LINES
# 
# df2dash = get_data_with_0_dashboard(df)
# df2dash.to_csv('data_dashboard.csv', index=False)
# 

# %%
df = df.sort_values(by='date')
# %%
df = df.reset_index()
a = df.copy()
df = filter_model_columns(df)
df_model = df.copy()
# %%
# Sort the dataframe by date

y, y_ = df_model.pop('visits'), df_model.pop('old_visits')
X = df_model
# %%


X_train, _, y_train, _ = train_test_split(
    X, y, test_size=0.2, shuffle=True, random_state=11)

_, X_test, _, y_test = train_test_split(
    X, y_, test_size=0.2, shuffle=True, random_state=11)


regr = Lasso(alpha=1)
regr.fit(X_train, y_train)

y_pred = regr.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print('-------------------')
print(mse)
print(regr.score(X_train, y_train))
print(regr.score(X_test, y_test))
# %%
get_sorted_coefs(df_model.columns, regr.coef_)

#%%

#mae = mean_absolute_error(y_test, y_pred) if you want it from the regression
#
#from stacking:
#   old_navy: 38.02
#   subway: 33.88
#   walmart: 233.84
#   starbucks: 54.13

mae = 38.02
df = get_data_with_0_dashboard(a)
df = workforce(df, brand)
df['workforce'] = np.where((df.visits == 0),0,df.workforce) 
df = IC_visits(df, mae)
df = income_visits(df, brand)
df = df.drop('index', axis = 1)
df.to_csv(f'{brand}_dashboard.csv', index=False)


#%%
df
# %%
"""
SVM -> very very very slow


#params = {'kernel': ['poly', 'rbf', 'sigmoid'],
#          'degree': [1, 3, 5],
#          'C': [0.5, 1, 1.5]}
#model = GridSearchCV(svm.SVR(), params)
"""

model = SVR(kernel='poly', degree=2, C=1)#(n_estimators=200, criterion='mse', n_jobs=-1)

model.fit(X_train, y_train)

y_pred = model.predict(X=X_test)

mse = mean_squared_error(y_test, y_pred)

print(f"El error (mse) de test es: {mse}")
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))
print(model.get_params())

#%%

# %%

# params = {'n_estimators': [20, 50, 100, 150, 200],
#          'criterion': ['mse', 'mae'],
#          'max_features': ['auto', 'sqrt', 'log2']}
# model = RandomizedSearchCV(RandomForestRegressor(),
#                           params,
#                           cv=2,
#                           n_jobs=-1)

model = RandomForestRegressor(
    n_estimators=100, criterion='mse', n_jobs=-1)  # 100 params are OK
model.fit(X_train, y_train)

y_pred = model.predict(X=X_test)

mse = mean_squared_error(y_test, y_pred)

print(f"El error (mse) de test es: {mse}")
print(model.score(X_train, y_train))
print(model.score(X_test, y_test))
print(model.get_params())

# %%
params = {'n_estimators': 500,
          'max_depth': 5,
          'min_samples_split': 5,
          'learning_rate': 0.01,
          'loss': 'ls'}

reg = GradientBoostingRegressor(**params)
reg.fit(X_train, y_train)

y_pred = reg.predict(X_test)
train_mse = mean_squared_error(y_train, reg.predict(X_train))
test_mse = mean_squared_error(y_test, reg.predict(X_test))
print(train_mse)
print(test_mse)

print(r2_score(y_train, reg.predict(X_train)))
print(r2_score(y_test, reg.predict(X_test)))
# %%


# %%
param = {'max_depth': 5, 'eta': 0.3, 'objective': 'reg:squarederror', 'eval_metric': 'rmse',
         'subsample': 0.9, 'colsample_bytree': 0.5}


dtrain = xgb.DMatrix(X_train, label=y_train)
bst = xgb.train(params=param, dtrain=dtrain)

dtest = xgb.DMatrix(X_test)
y_pred = bst.predict(dtest)

train_mse = mean_squared_error(y_train, bst.predict(dtrain))
test_mse = mean_squared_error(y_test, bst.predict(dtest))
print(train_mse)
print(test_mse)

print(r2_score(y_train, bst.predict(dtrain)))
print(r2_score(y_test, bst.predict(dtest)))

# %%
test_score = np.zeros((params['n_estimators'],), dtype=np.float64)
for i, y_pred in enumerate(reg.staged_predict(X_test)):
    test_score[i] = reg.loss_(y_test, y_pred)

fig = plt.figure(figsize=(6, 6))
plt.subplot(1, 1, 1)
plt.title('Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, reg.train_score_, 'b-',
         label='Training Set Deviance')
plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
         label='Test Set Deviance')
plt.legend(loc='upper right')
plt.xlabel('Boosting Iterations')
plt.ylabel('Deviance')
fig.tight_layout()
plt.show()

#%%
a

#%%
def income_visits(df, brand):
    df = df.copy()
    
    if brand == 'subway':
        df['income_visits'] = round(df['visits'] * 9.5).astype(int)
        df['min_income_visits'] = round(df['min_visits'] * 9.5).astype(int)
        df['max_income_visits'] = round(df['max_visits'] * 9.5).astype(int)
        
    elif brand == 'Starbucks':
        df['income_visits'] = round(df['visits'] * 4.10).astype(int)
        df['min_income_visits'] = round(df['min_visits'] * 4.10).astype(int)
        df['max_income_visits'] = round(df['max_visits'] * 4.10).astype(int)
    
    elif brand == 'Walmart':
        df['income_visits'] = round(df['visits'] * 55).astype(int)
        df['min_income_visits'] = round(df['min_visits'] * 55).astype(int)
        df['max_income_visits'] = round(df['max_visits'] * 55).astype(int)
    
    elif brand == 'old_navy':
        df['income_visits'] = round(df['visits'] * 50).astype(int)
        df['min_income_visits'] = round(df['min_visits'] * 50).astype(int)
        df['max_income_visits'] = round(df['max_visits'] * 50).astype(int)
        
    return df

def workforce(df, brand):
    df = df.copy()
    if brand == 'subway':
        df['workforce'] = round((df['visits'] * 4)/150).astype(int)
        df['workforce'] = np.where((df.workforce < 4),4,df.workforce)
        
    elif brand == 'Starbucks':
        df['workforce'] = round((df['visits'] * 4)/210).astype(int)
        df['workforce'] = np.where((df.workforce < 4),4,df.workforce)
    
    elif brand == 'Walmart':
        df['workforce'] = round((df['visits'] * 50)/2000).astype(int)
        df['workforce'] = np.where((df.workforce < 50),50,df.workforce)
       
    elif brand == 'old_navy':
        df['workforce'] = round((df['visits'] * 5)/250).astype(int)
        df['workforce'] = np.where((df.workforce < 5),5,df.workforce) 
    
    return df


def IC_visits(df, mae):
    df = df.copy()
    
    mean_visits = df['visits'].mean()
    mae_new = ((df['visits'] * mae) / mean_visits)
    
    df['min_visits'] = round(df['visits'] - mae_new)
    df['max_visits'] = round(df['visits'] + mae_new)
    
    return df
#%%
mae = mean_absolute_error(y_test, y_pred)
mae
#%%

b = workforce(a, brand)
b = IC_visits(b, mae)
b = income_visits(b, brand)
b
# %%
