# %%
import json
import os
from datetime import timedelta

import holidays
import pandas as pd
from utils.date_utils.date_formats import DATE_FORMATS
from utils.download_data import data_dtypes as dtypes
from utils.download_data import datasets
from utils.path_utils import paths

houston_folder = os.path.join(paths.processed_datasets,
                              "Houston")

houston_dataset_path = os.path.join(houston_folder,
                                    "mobility-patterns-backfilled_2020-01-01_2021-04-13.csv")
subway_path = os.path.join(houston_folder, "subway.csv")
rain_path = os.path.join(paths.processed_datasets,
                         "Houston",
                         "rain_houston.csv")


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


# %%
df_orginal = pd.read_csv(subway_path, encoding="utf-8",
                         dtype=dtypes.mobility_dtypes)
df_orginal = drop_duplicate_stores(df_orginal)
brand_info = datasets.get_brand_info_dataset()
core_poi = datasets.get_core_poi_by_city("Houston", "TX")
rain = pd.read_csv(rain_path)
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


df = explode_vists_by_day(df_orginal)
df = filter_selected_cols(df)
df = add_last_visits(df)
df
# %%


# %%
rain['date'] = pd.to_datetime(rain["date"], format=DATE_FORMATS.DAY)
df = df.merge(rain, on='date', how='left')

# %%
holi = holidays.CountryHoliday('US', prov="Houston", state='TX')
df["is_holiday"] = [1 if d in holi else 0 for d in df["date"]]
