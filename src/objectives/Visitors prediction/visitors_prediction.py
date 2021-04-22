# %%
import json
import os

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
subway_normalized = os.path.join(houston_folder, "subway_normalized.csv")
rain_path = os.path.join(paths.processed_datasets,
                         "Houston",
                         "rain_houston.csv")

# %%
df_orginal = pd.read_csv(subway_path, encoding="utf-8",
                         dtype=dtypes.mobility_dtypes)
brand_info = datasets.get_brand_info_dataset()
core_poi = datasets.get_core_poi_by_city("Houston", "TX")
rain = pd.read_csv(rain_path)
# %%


def normalize_vists_by_day(df_old):
    def get_dictionary_list_visits_day(visits_list):
        return [{"visits": visits, "day": day + 1} for day, visits in enumerate(visits_list)]
    df = df_old.copy()
    df["visits_by_day"] = df["visits_by_day"].apply(json.loads)
    df["date"] = pd.to_datetime([d.split("T")[0] for d in df["date_range_start"]],
                                format="%Y-%m-%d")
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["visits_by_day"] = [get_dictionary_list_visits_day(l)
                           for l in df["visits_by_day"]]
    df = df.explode(column="visits_by_day", ignore_index=True)
    info = pd.json_normalize(df["visits_by_day"])
    for c in info.columns:
        df[c] = info[c]
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


df = normalize_vists_by_day(df_orginal)
df = filter_selected_cols(df)
# %%
# %%
rain.columns = ['date', 'precip']
rain['date'] = pd.to_datetime(rain["date"], format=DATE_FORMATS.DAY)
# %%
df = df.merge(rain, on='date', how='left')

# %%
holi = holidays.CountryHoliday('US', prov="Houston", state='TX')
df["is_holiday"] = [1 if d in holi else 0 for d in df["date"]]
