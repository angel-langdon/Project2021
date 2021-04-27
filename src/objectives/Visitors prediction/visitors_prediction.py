# %%
import json
import os
from collections import Counter
from datetime import datetime, timedelta

import holidays
import numpy as np
import pandas as pd
from sklearn.linear_model import (BayesianRidge, ElasticNet, HuberRegressor,
                                  Lasso, LinearRegression, Ridge)
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from utils.date_utils.date_formats import DATE_FORMATS
from utils.download_data import data_dtypes as dtypes
from utils.download_data import datasets, download_safegraph_data
from utils.path_utils import paths


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
        df["poi_cbg"] = df["poi_cbg"].astype("int64").astype("category")
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


def add_income(df, city="Houston", state='TX'):
    df = df.copy()
    df["poi_cbg"] = df["poi_cbg"].astype(int).astype(str)
    file_name = "income.csv"
    path = paths.get_processed_file_path(state, city, file_name)
    # In case the file exist
    if os.path.isfile(path):
        income = pd.read_csv(path, dtype=dtypes.census_dtypes,
                             encoding="utf-8")
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

def mean_week(test):
    n = 7
    test['date'] = pd.to_datetime(test.date)
    idx = pd.date_range(test.date.min(), test.date.max(), freq='D')
    df_eee = test.pivot(index='date', values='visits', columns='placekey').reindex(idx)
    #print(df_eee.iloc[0])
    df2 =(df_eee.shift().rolling(window=n, min_periods=1).mean().reset_index().drop_duplicates())
    #print(df2['index'])
    df3 = (pd.melt(df2, id_vars='index', value_name='visits').sort_values(['index', 'placekey']).reset_index(drop=True))
    df3 = df3.rename(columns={'index':'date', 'visits':'mean_last_week'})
    test = test.merge(df3, on=['placekey', 'date'], how='left')
    return test

def mean_30_days(test):
    n = 30
    test['date'] = pd.to_datetime(test.date)
    idx = pd.date_range(test.date.min(), test.date.max(), freq='D')
    df_eee = test.pivot(index='date', values='visits', columns='placekey').reindex(idx)
    #print(df_eee.iloc[0])
    df2 =(df_eee.shift().rolling(window=n, min_periods=1).mean().reset_index().drop_duplicates())
    #print(df2['index'])
    df3 = (pd.melt(df2, id_vars='index', value_name='visits').sort_values(['index', 'placekey']).reset_index(drop=True))
    df3 = df3.rename(columns={'index':'date', 'visits':'mean_last_week'})
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

def filter_columns(df):
    df = df.copy()
    target_cols = ['placekey', "brands", 'latitude',
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
        
    df = (df.sort_values(["placekey", "date"]).groupby("placekey", as_index=False).bfill().ffill())
    
    return df

country = "US"
city = "Houston"
state = "TX"
brand = "subway"
df_original = read_patterns_data(city, state, brand)
df = explode_visits_by_day(df_original)
df = filter_columns(df)
df = add_week_columns(df)
df = add_income(df, city, state)
df = add_is_holiday(df, city, state, country)
df = add_rain(df, city, state)
df = add_population(df, city, state)
df = add_devices(df, city, state)
df = compute_real_visits(df)
df = add_last_visits(df)
df = mean_week(df)
df = mean_30_days(df)
#df = clean_stores(df)
#df = add_dummies(df, drop_first=False)
# %%


# %%
cols = ['date', 'visits']
test_df = df[df['placekey'] == '222-222@8fc-8ct-47q']
test_df = test_df[cols]
test_df = test_df.resample('W', on='date').mean()
test_df.head()


def add_mean_visits(df):
    df = df.sort_values(["placekey", "date"])

    pass

#%%

#%%
ccc
#%%
testing = ccc[ccc['placekey'] == '222-222@8fc-8ct-47q']

testing['visits'][0:7].mean()
#%%

testing.head(8)

#%%
def filter_model_columns(df: pd.DataFrame):
    exclude_cols = ['placekey',
                    'brands',
                    'latitude',
                    'longitude',
                    'street_address',
                    'date',
                    'week_day' ]
    cols = [col for col in df.columns if col not in exclude_cols]
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
# selection=['year_2020', 'year_2021', 'day', 'yesterday_visits', 'last_week_visits',
#             'is_weekend', 'cbg_income', 'is_holiday', 'rain', 'population', 'Monday', 'Tuesday',
#             'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
#             'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
#             'September', 'October', 'November', 'December']
df = df.sort_values(by='date')
df = filter_model_columns(df)
# %%
# Sort the dataframe by date

y = df.pop('visits')
X = df
# %%

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False)

regr = Lasso(alpha=1)
regr.fit(X_train, y_train)

y_pred = regr.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print('-------------------')
print(mse)
print(regr.score(X_train, y_train))
print(regr.score(X_test, y_test))
# %%
get_sorted_coefs(df.columns, regr.coef_)

# %%
"""
TESTING
"""

df
# %%
