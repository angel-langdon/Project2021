# %%
import os

import boto3
import pandas as pd
from utils.download_data import data_dtypes
from utils.path_utils import path_utils, paths
from utils.secrets.secrets import (SAFEGRAPH_ACCESS_KEY_ID, SAFEGRAPH_BUCKET,
                                   SAFEGRAPH_ENDPOINT_URL,
                                   SAFEGRAPH_REGION_NAME,
                                   SAFEGRAPH_SECRET_ACCESS_KEY,
                                   SAFEGRAPH_SERVICE_NAME)


# %%
class SafeGraphSession():
    def __init__(self, prefix, bucket_name):
        self.access_key_id = SAFEGRAPH_ACCESS_KEY_ID
        self.secret_access_key = SAFEGRAPH_SECRET_ACCESS_KEY
        self.service_name = SAFEGRAPH_SERVICE_NAME
        self.bucket_name = SAFEGRAPH_BUCKET
        self.endpoint = SAFEGRAPH_ENDPOINT_URL
        self.region_name = SAFEGRAPH_REGION_NAME
        self.prefix = prefix
        self.all_files = None
        self.files_filtered_by_month = None

        self.session = boto3.Session(
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region_name)
        self.client = self.session.client(self.service_name,
                                          endpoint_url=self.endpoint)
        self.bucket = self.session.resource(self.service_name,
                                            endpoint_url=self.endpoint).Bucket(bucket_name)

    def list_all_files(self):
        if self.all_files:
            return self.all_files
        else:
            files = [elm.key for elm in self.bucket.objects.all() if elm.key.startswith(self.prefix)
                     and (elm.key.endswith('.csv') or elm.key.endswith('.csv.gz'))]
            self.all_files = files
            return files

    def filter_files_by_month(self, files=None):
        if self.files_filtered_by_month:
            return self.files_filtered_by_month

        if not files:
            files = self.list_all_files()

        date_dict = {}
        for f in files:
            s = f.split('/')
            if 'backfill' in s[1]:
                date = s[-3] + '-' + s[-2]
                if date in date_dict.keys():
                    date_dict[date] = date_dict[date] + [f]
                else:
                    date_dict[date] = [f]
            else:
                m = int(s[-4])
                y = s[-5]
                if m == 1:
                    m = '12'
                    y = str(int(y)-1)
                elif m > 10:
                    m = str(m-1)
                else:
                    m = '0' + str(m-1)
                date = y + '-' + m
                if date in date_dict.keys():
                    date_dict[date] = date_dict[date] + [f]
                else:
                    date_dict[date] = [f]

        self.files_filtered_by_month = date_dict
        return self.files_filtered_by_month

    def download_file(self, bucket_path: str, dest_path: str = None,
                      append_datasets_path: bool = True,
                      verbose: bool = False):
        if not dest_path:
            dest_path = bucket_path
        if append_datasets_path:
            dest_path = os.path.join(paths.DATASETS, dest_path)

        path_utils.create_dir_if_necessary(dest_path)

        if verbose:
            print(f"Saving file in: {dest_path}")
        if not os.path.isdir(dest_path):
            self.client.download_file(self.bucket_name, bucket_path, dest_path)


prefix = 'monthly-patterns-2020-12'
bucket = "sg-c19-response"
session = SafeGraphSession(prefix, bucket)
files = session.list_all_files()
# %%

# files_filtered_by_month = session.filter_files_by_month()
# for file in files_filtered_by_month["2021-02"]:
#     session.download_file(file)

# %%
location = "Los Angeles"
datasets_location = os.path.join(location, paths.DATASETS)
files_filter_by_month = session.filter_files_by_month()
files = [os.path.join(paths.DATASETS, f)
         for f in files_filter_by_month["2021-02"] if "patterns-part" in f]

for file in files:

    print(file)
# %%
% % time
chunks = []
for file in files:
    for i, chunk in enumerate(pd.read_csv(file,
                                          sep=",",
                                          chunksize=10000,
                                          engine='c',
                                          low_memory=False)):
        chunks.append(chunk[chunk["city"] == location].copy())
        if i == 10:
            break
    break
# %%
df_los_angeles = pd.concat(chunks, axis=0)
df_los_angeles = df_los_angeles.astype(data_dtypes.mobility_dtypes)
# %%
df_los_angeles.memory_usage(deep=True)/1024**2
# %%
data_dtypes.mobility_dtypes
# %%
