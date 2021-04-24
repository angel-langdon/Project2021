# %%
import os

from utils.download_data import download_safegraph_data
from utils.path_utils import path_utils

datasets_folder_name = "datasets"
temp_folder_name = "temp"
processed_folder_name = "processed"
python_lib_folder = "PythonLib"
max_recursion_limit = 30


def get_datasets_path(dir: str = ".", recursion_level: int = 0) -> str:
    possible_path: str = os.path.join(dir, python_lib_folder)
    if os.path.isdir(possible_path):
        datasets_path = os.path.abspath(os.path.join(dir,
                                                     datasets_folder_name))
        path_utils.create_dir_if_necessary(datasets_path)
        return datasets_path
    if recursion_level > max_recursion_limit:
        raise BaseException(f"Datasets path not found {datasets_folder_name}")
    return get_datasets_path(os.path.join("..", dir), recursion_level + 1)


def get_processed_file_path(state, city, file_name):
    return os.path.join(processed_datasets, state, city, file_name)


def get_census_path(file_name):
    path = os.path.join(open_census_dir, "data", file_name)
    if not os.path.isdir(open_census_dir):
        download_safegraph_data.download_census_data()
    return path


DATASETS = get_datasets_path()
temp_datasets = os.path.join(DATASETS, temp_folder_name)
processed_datasets = os.path.join(DATASETS, processed_folder_name)
core_places_delivery = os.path.join(DATASETS, "core-places-delivery")
core_poi = os.path.join(core_places_delivery,
                        "core_poi")
brand_info = os.path.join(core_places_delivery,
                          "brand_info")

open_census_dir = os.path.join(DATASETS,
                               "open-census-data",
                               "safegraph_open_census_data")
# %%
