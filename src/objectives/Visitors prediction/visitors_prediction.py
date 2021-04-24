# %%
import json
import os
from datetime import timedelta

import holidays
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
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
        df["poi_cbg"] = df["poi_cbg"].astype(int).astype("category")
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


def is_holiday(df, city='Houston', state='TX', country='US'):
    df = df.copy()
    holi = holidays.CountryHoliday(country, prov=city, state=state)
    df["is_holiday"] = [1 if d in holi else 0 for d in df["date"]]
    return df


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


# "NEEDED THE PATH OF THE POPULATION.CSV, DEVICES.CSV, SUBWAY_HOUSTON_DAYS (SUBWAY)"


def get_population(df, city, state):
    df = df.copy()
    file_name = 'population.csv'
    possible_path = os.path.join(paths.processed_datasets,
                                 state, city, file_name)
    if os.path.isfile(possible_path):
        pop = pd.read_csv(possible_path)
        pop['poi_cbg'] = pop['poi_cbg'].astype(int).astype(str)
        return df.merge(pop, on='poi_cbg', how='left')
    else:
        msg = 'Population dataset not found, should be here:\n'+possible_path
        raise(FileNotFoundError(msg))


def get_devices(df, city, state):
    df = df.copy()
    file_name = "devices.csv"
    possible_path = os.path.join(paths.processed_datasets,
                                 state, city, file_name)
    if os.path.isfile(possible_path):
        # home_panel_summary
        nf = pd.read_csv(os.path.join(paths.processed_datasets,
                                      "Houston",
                                      "devices.csv"))
        nf['poi_cbg'] = nf['poi_cbg'].astype(int).astype(str)
        return df.merge(nf, on='poi_cbg', how='left')
    else:
        msg = "Devices data not found, should be here:\n"+possible_path
        raise(FileNotFoundError(msg))


def get_real_visits(df):
    df['real_visits'] = (df['population'] // df['devices'])*df['visits']
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
df

# %%
df = get_population(df)
df = get_devices(df)
df = get_real_visits(df)
df = add_last_visits(df)

# %%

df.to_csv(os.path.join(paths.processed_datasets,
                       "Houston",
                       "MODEL_SUBWAY.csv"), index=False)
# %%


def add_dummies_df(df_: pd.DataFrame):

    df = df_.copy()
    dummies = pd.get_dummies(df['year'], prefix='year')
    # Drop column B as it is now encoded
    df = df.drop('year', axis=1)
    # Join the encoded df
    df = df.join(dummies)

    dummies = pd.get_dummies(df['month'])
    # Drop column B as it is now encoded
    df = df.drop('month', axis=1)
    # Join the encoded df
    dummies.columns = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
    df = df.join(dummies)

    dummies = pd.get_dummies(df['week_day'])
    # Drop column B as it is now encoded
    df = df.drop('week_day', axis=1)
    # Join the encoded df
    dummies.columns = ['Monday', 'Tuesday', 'Wednesday',
                       'Thursday', 'Friday', 'Saturday', 'Sunday']
    df = df.join(dummies)

    return df

# %%


"""
VERY IMPORTANT, CONTACT WITH n4choo, zMazcu or MikeKowalski for futher information
"""

df = pd.read_csv(os.path.join(paths.processed_datasets,
                              "Houston",
                              "MODEL_SUBWAY.csv"))

df = df[(df['date'] > '2020-03-15')]

placekeys_series = df['placekey'].value_counts()
placekeys_series = placekeys_series[placekeys_series >= 200]
placekeys = list(placekeys_series.index)

df = df[df['placekey'].isin(placekeys)]

df = df[df['real_visits'] != 0]

df = df.sort_values(by='date')
# %%
"""
SEEMS STUPID, BUT IT IS CRUCIAL FOR THE MODEL
"""
df['yesterday_visits'] = df['yesterday_visits'].replace(0.0, np.NaN)
df['last_week_visits'] = df['last_week_visits'].replace(0.0, np.NaN)

# %%

"""
-----------------------------------------------------
----------------------M O D E L----------------------
-----------------------------------------------------
"""


"""
selection = ['year', 'month', 'day', 'yesterday_visits', 'last_week_visits',
             'week_day', 'is_weekend', 'cbg_income', 'is_holiday', 'rain', 'population']
"""
selection = ['year_2020', 'year_2021', 'day', 'yesterday_visits', 'last_week_visits',
             'is_weekend', 'cbg_income', 'is_holiday', 'rain', 'population', 'Monday', 'Tuesday',
             'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
             'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
             'September', 'October', 'November', 'December']

df_model = add_dummies_df(df)
df_model = df_model.fillna(method='backfill')
df_model = df_model.fillna(method='ffill')


y = df_model.pop('real_visits')
X = df_model[selection]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, shuffle=False, random_state=20)

clf = Ridge(alpha=1.0)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

print(mse)
# %%
print(clf.score(X_train, y_train))
print(clf.score(X_test, y_test))
# %%
