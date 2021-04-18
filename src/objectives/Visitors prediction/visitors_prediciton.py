# %%
import os

import pandas as pd
from utils.download_data import data_dtypes as dtypes
from utils.path_utils import paths

houston_folder = os.path.join(paths.processed_datasets,
                              "Houston")

houston_dataset_path = os.path.join(houston_folder,
                                    "mobility-patterns-backfilled_2020-01-01_2021-04-13.csv")
# %%
df = pd.read_csv(houston_dataset_path,
                 dtype=dtypes.mobility_dtypes)

# %%
subway_path = os.path.join(houston_folder, "subway.csv")
subway = pd.read_csv(subway_path, encoding="utf-8",
                     dtype=dtypes.mobility_dtypes)

# %%


subway

# %%
