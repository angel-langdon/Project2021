# %%
import json
import os
from datetime import timedelta

import holidays
import numpy as np
import pandas as pd
from utils.date_utils.date_formats import DATE_FORMATS
from utils.download_data import data_dtypes as dtypes
from utils.path_utils import paths

houston_folder = os.path.join(paths.processed_datasets,
                              "Houston")

houston_dataset_path = os.path.join(houston_folder,
                                    "mobility-patterns-backfilled_2020-01-01_2021-04-13.csv")
subway_path = os.path.join(houston_folder, "subway.csv")
rain_path = os.path.join(paths.processed_datasets,
                         "Houston",
                         "rain_houston.csv")

#%%
def drop_duplicate_stores(patterns: pd.DataFrame):
    """ Drops duplicated rows of patterns data
    """
    df = patterns.copy()
    df = df.sort_values(by=["placekey",
                            "date_range_start"])
    df = df.drop_duplicates(subset=["placekey",
                                    "date_range_start",
                                    "date_range_end"],
                            keep="last")
    return df


def read_patterns_data(path):
    df = pd.read_csv(path, encoding="utf-8",
                     dtype=dtypes.mobility_dtypes)
    df = drop_duplicate_stores(df)
    return df


# %%
df_original = read_patterns_data(subway_path)
#rain = pd.read_csv(rain_path)
# %%

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
        period_df[period_visits_col] = df["real_visits"]
        df = pd.merge(df, period_df, how="left",
                      on=["placekey", "date"])
        # drop the column from the auxiliar dataframe in case
        # there are more date periods to add
        period_df = period_df.drop(columns=[period_visits_col])
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

"""
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
"""

def is_holiday(df):
    df.copy()
    holi = holidays.CountryHoliday('US', prov="Houston", state='TX')
    df["is_holiday"] = [1 if d in holi else 0 for d in df["date"]]
    return df

def income(df):
    cosa = pd.read_csv(os.path.join(paths.processed_datasets,
                         "Houston",
                         "income.csv"), encoding="utf-8",
                       dtype={"census_block_group": "category"})

    df['poi_cbg'] = df['poi_cbg'].map(int)
    df['poi_cbg'] = df['poi_cbg'].map(str)

    #new = df[df['region'] == 'TX']
    cbgs = set(df['poi_cbg'])

    cosa = cosa[cosa['census_block_group'].map(int).map(str).isin(cbgs)]
    # cosa = cosa[['census_block_group', 'B19013e1']]
    cosa.columns = ['poi_cbg', 'cbg_income']
    #cosa.rename({'census_block_group': 'poi_cbg', 'B19013e1': 'cbg_income'})
    cosa['poi_cbg'] = cosa['poi_cbg'].astype(int).astype(str)
    df = df.merge(cosa, on='poi_cbg', how='left')
    return df

    """
    new['cbg_income'] = 0
    for row in cosa.iterrows():
        new['cbg_income'] = np.where(new['poi_cbg'] == str(
            row[1][0]), row[1][1], new['cbg_income'])

    return new
    """

"""ERROR"""

def rain(df):
    rain_ = pd.read_csv(rain_path)
    #rain_2020 = pd.read_csv('data/rain_houston_2020.csv', sep=';')
    #rain_2021 = pd.read_csv('data/rain_houston_2021.csv', sep=';')
    # df['date'] = df['date'].map(int)
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    rain_['Dates'] = pd.to_datetime(rain_['Dates'])
    rain_['Dates'] = rain_['Dates'].dt.strftime('%Y-%m-%d')
    rain_.columns = ['date', 'rain']
    #print(rain['date'])
    df = df.merge(rain_, on='date', how='left')
    return df

#"NEEDED THE PATH OF THE POPULATION.CSV, DEVICES.CSV, SUBWAY_HOUSTON_DAYS (SUBWAY)"


def get_population(df):
    dat = pd.read_csv(os.path.join(paths.processed_datasets,
                         "Houston",
                         "population.csv"))
    dat['poi_cbg'] = dat['poi_cbg'].astype(int).astype(str)
    df['poi_cbg'].astype(int).astype(str)
    df = df.merge(dat, on='poi_cbg', how='left')
    return df


def get_devices(df):
    # home_panel_summary
    nf = pd.read_csv(os.path.join(paths.processed_datasets,
                         "Houston",
                         "devices.csv"))
    nf['poi_cbg'] = nf['poi_cbg'].astype(int).astype(str)
    df['poi_cbg'].astype(int).astype(str)
    #print(type(df['poi_cbg']), type(nf['poi_cbg']))
    df = df.merge(nf, on='poi_cbg', how='left')

    return df


def get_real_visits(df):
    df['real_visits'] = (df['population'] // df['devices'])*df['visits']
    return df


df = explode_vists_by_day(df_original)
df = filter_selected_cols(df)

df = add_week_columns(df)
df = income(df)
df = is_holiday(df)
df = rain(df)
df = get_population(df)
df = get_devices(df)
df = get_real_visits(df)
df = add_last_visits(df)

# %%

df.to_csv('MODEL_SUBWAY.csv', index = False)

#%%

df = pd.read_csv(os.path.join(paths.processed_datasets,
                         "Houston",
                         "MODEL_SUBWAY.csv"))
# %% 

def add_dummies_df(df_: pd.DataFrame):

    df = df_.copy()
    dummies = pd.get_dummies(df['year'], prefix='year')
    # Drop column B as it is now encoded
    df = df.drop('year', axis = 1)
    # Join the encoded df
    df = df.join(dummies)
    
    dummies = pd.get_dummies(df['month'])
    # Drop column B as it is now encoded
    df = df.drop('month', axis = 1)
    # Join the encoded df
    dummies.columns = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df = df.join(dummies)

    dummies = pd.get_dummies(df['week_day'])
    # Drop column B as it is now encoded
    df = df.drop('week_day', axis = 1)
    # Join the encoded df
    dummies.columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df = df.join(dummies)

    return df
#%%
df_model = add_dummies_df(df)

# %%
# RIDGE LINEAR REGRESSION

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

"""
selection = ['placekey', 'year', 'month', 'day', 'yesterday_visits', 'last_week_visits',
             'week_day', 'is_weekend', 'cbg_income', 'is_holiday', 'rain', 'population']
"""
selection = ['year_2020', 'year_2021', 'day', 'yesterday_visits', 'last_week_visits',
             'is_weekend', 'cbg_income', 'is_holiday', 'rain', 'population', 'Monday', 'Tuesday', 
             'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 
             'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
             'September', 'October', 'November', 'December']

df_model = df_model.fillna(method='backfill')

y = df_model.pop('real_visits')
X = df_model[selection]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False,random_state=20)

clf = Ridge(alpha=1.0)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

print(y_pred)


# %%
print(clf.score(X_test, y_test, sample_weight=None))

# %%

df = pd.read_csv(os.path.join(paths.processed_datasets,
                         "Houston",
                         "MODEL_SUBWAY.csv"))

df = df[(df['date'] > '2020-03-15')]

placekeys_series = df['placekey'].value_counts()
placekeys_series = placekeys_series[placekeys_series >= 200]
placekeys = list(placekeys_series.index)

a = df[df['placekey'].isin(placekeys)]

a = a[a['real_visits'] != 0]

a = a.sort_values(by='date')
# %%
a['yesterday_visits'] = a['yesterday_visits'].replace(0.0, np.NaN)
a['last_week_visits'] = a['last_week_visits'].replace(0.0, np.NaN)

# %%

"""

----------------------M O D E L----------------------

"""


from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

"""
selection = ['placekey', 'year', 'month', 'day', 'yesterday_visits', 'last_week_visits',
             'week_day', 'is_weekend', 'cbg_income', 'is_holiday', 'rain', 'population']
"""
selection = ['year_2020', 'year_2021', 'day', 'yesterday_visits', 'last_week_visits',
             'is_weekend', 'cbg_income', 'is_holiday', 'rain', 'population', 'Monday', 'Tuesday', 
             'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 
             'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
             'September', 'October', 'November', 'December']

a = add_dummies_df(a)
df_model = a.fillna(method='backfill')
df_model = df_model.fillna(method='ffill')


y = df_model.pop('real_visits')
X = df_model[selection]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False,random_state=20)

clf = Ridge(alpha=1.0)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

print(mse)
# %%
print(clf.score(X_train, y_train))
print(clf.score(X_test, y_test))
# %%
