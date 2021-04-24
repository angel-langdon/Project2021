# %%
import os
from typing import List

import pandas as pd
from utils.download_data import data_dtypes as dtypes
from utils.download_data import download_safegraph_data
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


def filter_census_df(path: str, columns: List[str], cbgs: List[str]):
    """ Filters census .csv given the columns and the cbgs
    """
    dfs = []
    # read the file per parts because it is 1gb large
    for chunk in pd.read_csv(path,
                             encoding="utf-8",
                             chunksize=10000,
                             dtype=dtypes.census_dtypes):
        chunk["census_block_group"] = (chunk["census_block_group"]
                                       .astype(int).astype(str))
        chunk = chunk[chunk["census_block_group"].isin(cbgs)]
        chunk = chunk[columns]
        dfs.append(chunk.copy())
    # concat the filtered chunks
    return pd.concat(dfs)


def get_census_metadata():
    files = [f for f in path_utils.list_files_recursively(paths.open_census_dir)
             if file_type.is_census_metadata(f)]
    for file in files:
        if "description" in file:
            break
    return pd.read_csv(file)


def get_lastest_home_pannel_summary(cbgs=None, donwload_most_recent=True):
    if donwload_most_recent:
        path = download_safegraph_data.download_lastest_home_pannel_summary()

    if cbgs is not None:
        return filter_census_df(path, ["census_block_group",
                                "number_devices_residing"],
                                cbgs)
    return pd.read_csv(path, encoding="utf-8")


# %%
