# %%
import json
import os
from datetime import datetime, timedelta

import holidays
import numpy as np
import pandas as pd
from sklearn.linear_model import (BayesianRidge, ElasticNet, HuberRegressor,
                                  Lasso, Ridge)
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from utils.date_utils.date_formats import DATE_FORMATS
from utils.download_data import data_dtypes as dtypes
from utils.download_data import datasets
from utils.path_utils import paths


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
    possible_path = os.path.join(paths.processed_datasets,
                                 state, city, brand+".csv")
    if os.path.isfile(possible_path):
        df = pd.read_csv(possible_path, encoding="utf-8",
                         dtype=dtypes.mobility_dtypes)
        df["poi_cbg"] = df["poi_cbg"].astype("int64").astype("category")
        df = drop_duplicate_stores(df)
    else:
        msg = "Patterns data not found, should be here:\n"+possible_path
        raise(FileNotFoundError(msg))
    return df


def explode_vists_by_day(df_old):
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


def filter_selected_cols(df):
    df = df.copy()
    selected_cols = ['placekey', "brands", 'latitude',
                     'longitude', 'street_address', 'postal_code',
                     'poi_cbg', 'naics_code', 'date', 'year', 'month',
                     'day', 'visits']
    return df[selected_cols]


def add_week_columns(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    df["week_day"] = df["date"].dt.day_name()
    df['is_weekend'] = 0
    weekends_day = ["Saturday", "Sunday"]
    for day in weekends_day:
        df.loc[df['week_day'] == day, 'is_weekend'] = 1
    return df


def is_holiday(df, city='Houston', state='TX', country='US'):
    df = df.copy()
    holi = holidays.CountryHoliday(country, prov=city, state=state)
    df["is_holiday"] = [1 if d in holi else 0 for d in df["date"]]
    return df


def add_rain(df, city="Houston", state="TX"):
    possible_path = os.path.join(paths.processed_datasets,
                                 state, city, "rain.csv")
    if os.path.isfile(possible_path):
        rain_df = pd.read_csv(possible_path)
        rain_df['date'] = pd.to_datetime(rain_df['date'],
                                         format=DATE_FORMATS.DAY)
        return df.merge(rain_df, on='date', how='left')
    else:
        msg = "Rain data is missing it shoud be here: \n"+possible_path
        raise(BaseException(msg))


def add_income(df, city="Houston", state='TX'):
    df = df.copy()
    df["poi_cbg"] = df["poi_cbg"].astype(int).astype(str)
    processed_file_name = "income.csv"
    possible_path = os.path.join(paths.processed_datasets,
                                 state, city, processed_file_name)
    # In case the file exist
    if os.path.isfile(possible_path):
        income = pd.read_csv(possible_path, dtype=dtypes.census_dtypes,
                             encoding="utf-8")
        income["poi_cbg"] = income["poi_cbg"].astype(int).astype(str)
        return df.merge(income, on='poi_cbg', how="left")

    # else: In case the file doesn't exist
    census_path = os.path.join(paths.open_census_dir, "data",
                               "cbg_b19.csv")
    income = datasets.filter_census_df(census_path,
                                       ['census_block_group', 'B19013e1'],
                                       df["poi_cbg"].unique())
    # rename the cols for convenience
    income = income.rename(columns={"census_block_group": "poi_cbg",
                                    'B19013e1': 'cbg_income'})
    # save the dataframe to cache it for the next time
    income.to_csv(possible_path, index=False, encoding="utf-8")
    return df.merge(income, on='poi_cbg', how='left')


def add_population(df, city, state):
    df = df.copy()
    file_name = 'population.csv'
    possible_path = os.path.join(paths.processed_datasets,
                                 state, city, file_name)
    if os.path.isfile(possible_path):
        pop = pd.read_csv(possible_path)
        pop['poi_cbg'] = pop['poi_cbg'].astype(int).astype(str)
        return df.merge(pop, on='poi_cbg', how='left')
    else:
        census_path = os.path.join(paths.open_census_dir,
                                   "data",
                                   "cbg_b01.csv")
        pop_id = "B01001e1"
        cbgs = df["poi_cbg"].unique()
        pop = datasets.filter_census_df(census_path,
                                        ["census_block_group", pop_id],
                                        cbgs)
        pop = pop.rename(columns={pop_id: 'population',
                                  "census_block_group": 'poi_cbg'})
        pop['poi_cbg'] = pop['poi_cbg'].astype(int).astype(str)
        pop.to_csv(possible_path, index=False, encoding="utf-8")
        return df.merge(pop, on='poi_cbg', how="left")


def add_devices(df, city, state):
    df = df.copy()
    file_name = "devices.csv"
    possible_path = os.path.join(paths.processed_datasets,
                                 state, city, file_name)
    if os.path.isfile(possible_path):
        # home_panel_summary
        devices = pd.read_csv(possible_path)
        devices['poi_cbg'] = devices['poi_cbg'].astype(int).astype(str)
        return df.merge(devices, on='poi_cbg', how='left')
    else:
        devices = datasets.get_lastest_home_pannel_summary(df["poi_cbg"])
        devices = devices.rename(columns={"census_block_group": "poi_cbg"})
        devices["poi_cbg"] = devices["poi_cbg"].astype(int).astype(str)
        devices.to_csv(possible_path, index=False, encoding="utf-8")
        return df.merge(devices, on="poi_cbg", how="left")


def get_real_visits(df):
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


def add_dummies(df):
    df = df.copy()
    df = pd.get_dummies(df, columns=["year"])
    df["month"] = df["date"].dt.month_name()
    df = pd.get_dummies(df, columns=["month"])
    df["day"] = df["date"].dt.day_name()
    df = pd.get_dummies(df, columns=["day"])
    return df


country = "US"
city = "Houston"
state = "TX"
brand = "subway"
df_original = read_patterns_data(city, state, brand)
df = explode_vists_by_day(df_original)
df = filter_selected_cols(df)

df = add_week_columns(df)
df = add_income(df, city, state)
df = is_holiday(df, city, state)
df = add_rain(df, city, state)
df = add_population(df, city, state)
df = add_devices(df, city, state)
df = get_real_visits(df)
df = add_last_visits(df)
df = add_dummies(df)
df
# %%
for c in df.columns:
    print(c)


# %%
# Get rid of COVID window
df = df[(df['date'] > datetime(year=2020, month=3, day=15)]
# We delete the stores that have less than 200 observations
df=df[df.groupby('placekey')['placekey'].transform('size') > 200]
# It makes no sense for the model trying to predict 0 visits
# because 0 visits reflects that probably the store was closed
df=df[df['visits'] != 0]
# It is important to fill the values that have 0 with NAs
# to backfill them later, if we delete the values that are 0
# then we will loss 14000 rows more
df['yesterday_visits']=df['yesterday_visits'].replace(0.0, np.NaN)
df['last_week_visits']=df['last_week_visits'].replace(0.0, np.NaN)

# %%
"""
selection = ['year', 'month', 'day', 'yesterday_visits', 'last_week_visits',
             'week_day', 'is_weekend', 'cbg_income', 'is_holiday', 'rain', 'population']
"""
selection=['year_2020', 'year_2021', 'day', 'yesterday_visits', 'last_week_visits',
             'is_weekend', 'cbg_income', 'is_holiday', 'rain', 'population', 'Monday', 'Tuesday',
             'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
             'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
             'September', 'October', 'November', 'December']

# Sort the dataframe by date to create train test splits
df=df.sort_values(by='date')
# df_model = add_dummies_df(df)
df_model=df.fillna(method='backfill')
df_model=df_model.fillna(method='ffill')


y=df_model.pop('visits')
X=df_model
# %%

X_train, X_test, y_train, y_test=train_test_split(
    X, y, test_size=0.2, shuffle=False)

regr=Lasso(alpha=1)
regr.fit(X_train, y_train)

y_pred=regr.predict(X_test)

mse=mean_squared_error(y_test, y_pred)
print('-------------------')
print(mse)
print(regr.score(X_train, y_train))
print(regr.score(X_test, y_test))

# %%
