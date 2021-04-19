# %%
import ast
import os

import pandas as pd
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
df_normalized = pd.read_csv(subway_normalized, dtype=dtypes.mobility_dtypes)
# %%


def clean_date(date):
    return date[0:10]


def generate_days(date_range_start, visits_by_day):
    date = clean_date(date_range_start)
    year_month = date[0:7]
    visits = ast.literal_eval(visits_by_day)
    for i in range(len(visits)):
        new_day = f'{year_month}-{i+1}'
        yield new_day, i


def explode_visits(visits_by_day):
    visits = ast.literal_eval(visits_by_day)
    for visit in visits:
        yield visit


def mapping_visits_days(row):
    selected_col = ['placekey', 'safegraph_place_id', 'latitude',
                    'longitude', 'street_address', 'postal_code',
                    'poi_cbg', 'naics_code', 'date', 'year', 'month',
                    'day', 'visits']
    df = pd.DataFrame(columns=selected_col)
    for (date, day), visit in zip(generate_days(row["date_range_start"], row["visits_by_day"]),
                                  explode_visits(row["visits_by_day"])):
        values_to_add = {'placekey': [row['placekey']],
                         'safegraph_place_id': [row['safegraph_place_id']],
                         'latitude': [row['latitude']],
                         'longitude': [row['longitude']],
                         'street_address': [row['street_address']],
                         'postal_code': [row['postal_code']],
                         'poi_cbg': [row['poi_cbg']],
                         'naics_code': [row['naics_code']],
                         'date': [date],
                         'year': [date[0:4]],
                         'month': [date[5:7]],
                         'day': [day],
                         'visits': [visit]}

        df_aux = pd.DataFrame(values_to_add)
        df = pd.concat([df, df_aux], ignore_index=True)

    return df


# %%
# No la ejecuteis nunca más (porfavor)
# df = df_orginal.apply(mapping_visits_days, axis=1)
# lista_dataframes = [d for d in df]
# df = pd.concat(lista_dataframes)
#
# %%
# %%
df_normalized["date"] = pd.to_datetime(df_normalized["date"],
                                       format="%Y-%m-%d")

# %%
rain.columns = ['date', 'precip']
rain['date'] = pd.to_datetime(rain["date"], format="%Y-%m-%d")
# %%

df_normalized
df_normalized = df_normalized.merge(rain, on='date', how='left')

# %%

df_normalized['precip'].isna().sum()
