# %%
import os

import pandas as pd
from utils.download_data import data_dtypes as dtypes
from utils.file_utils import file_type
from utils.path_utils import path_utils, paths


def get_brand_info_dataset():
    for f in path_utils.list_files_recursively(paths.brand_info):
        df = pd.read_csv(f)
        return df


def get_core_poi_by_city(city, region=None, save_data=True):
    file_name = os.path.join(paths.processed_datasets,
                             city,
                             "core_poi.csv")
    if os.path.isfile(file_name):
        return pd.read_csv(file_name, encoding="utf-8")

    chunks = []
    for f in path_utils.list_files_recursively(paths.core_poi):
        for chunk in pd.read_csv(f, chunksize=10_000):
            city = "Houston"
            region = "TX"
            chunk = chunk[chunk["city"] == city]
            if region != None:
                chunk = chunk[chunk["region"] == region]
            chunks.append(chunk)
    final_df = pd.concat(chunks)
    if save_data:
        path_utils.create_dir_if_necessary(file_name)
        final_df.to_csv(file_name, encoding="utf-8", index=False)
    return final_df


# %%
files = [f for f in path_utils.list_files_recursively(paths.open_census_dir)
         if file_type.is_census_data(f)]
houston_folder = os.path.join(paths.processed_datasets, "Houston")
subway_normalized = os.path.join(houston_folder, "subway_normalized.csv")
df_normalized = pd.read_csv(subway_normalized, dtype=dtypes.mobility_dtypes)
# %%
file = files[0]
census = pd.read_csv(file, dtype=dtypes.census_dtypes)
# %%
census[census["census_block_group"].isin(df_normalized["poi_cbg"])]
# %%


def get_census_metadata():
    files = [f for f in path_utils.list_files_recursively(paths.open_census_dir)
             if file_type.is_census_metadata(f)]
    for file in files:
        if "description" in file:
            break
    return pd.read_csv(file)


# %%

# %%
