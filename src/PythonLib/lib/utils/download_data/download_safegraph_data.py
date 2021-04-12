# %%
import os
from datetime import datetime

import boto3
import pandas as pd
from utils.date_utils.date_formats import DATE_FORMATS
from utils.download_data import data_dtypes
from utils.file_utils import file_type, file_utils
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

    def list_all_files(self, list_everything=False):
        if self.all_files:
            return self.all_files
        else:
            if list_everything:
                files = [elm.key for elm in self.bucket.objects.all()]
            else:
                files = [elm.key for elm in self.bucket.objects.all() if elm.key.startswith(self.prefix)
                         and (elm.key.endswith('.csv') or elm.key.endswith('.gz'))]
            self.all_files = files
            return files

    def filter_files_by_month(self, files=None, as_dataframe=False):
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
        if as_dataframe:
            rows = [{"date": datetime.strptime(key, "%Y-%m"),
                     "files": value}
                    for key, value in date_dict.items()]
            self.files_filtered_by_month = pd.DataFrame(rows)
        else:
            self.files_filtered_by_month = date_dict
        return self.files_filtered_by_month

    def download_file(self, bucket_path: str, dest_path: str = None,
                      append_datasets_path: bool = True,
                      verbose: bool = False):
        if not dest_path:
            dest_path = bucket_path
        if append_datasets_path:
            dest_path = os.path.join(paths.DATASETS, dest_path)
        if not os.path.isfile(dest_path):
            path_utils.create_dir_if_necessary(dest_path)

            if verbose:
                print(f"Saving file in: {dest_path}")
            if not os.path.isdir(dest_path):
                self.client.download_file(self.bucket_name,
                                          bucket_path, dest_path)


def download_census_data():
    prefix = 'open-census-data'
    bucket = "sg-c19-response"
    session = SafeGraphSession(prefix, bucket)
    files = session.list_all_files()
    session.download_file(files[0])


def download_monthly_patterns_city_data(target_city: str,
                                        date_start: datetime,
                                        date_end: datetime = None,
                                        remove_original_files_after_download: bool = True,
                                        verbose: bool = True):

    if not date_end:
        date_end = datetime.now()
    prefix = 'monthly-patterns-2020-12'
    bucket = "sg-c19-response"
    session = SafeGraphSession(prefix, bucket)
    df = session.filter_files_by_month(as_dataframe=True)

    df = df[(df["date"] >= date_start) & (df["date"] <= date_end)]
    files = [f for f in df.explode("files")["files"]
             if file_type.is_mobility_pattern(f)]
    dfs = []
    for file in files:
        temp_file = os.path.join(paths.temp_datasets, file)
        session.download_file(file, temp_file, verbose=verbose)
        # read the file in chunks filter it and store in a list of dataframes
        if verbose:
            print("Reading: "+file)
        temp_file_path = ""
        for chunk in pd.read_csv(temp_file, encoding="utf-8", sep=",", chunksize=10000):
            filtered = chunk[chunk["city"] == target_city].copy()
            dfs.append(filtered)
        # once readed delete the file to free memmory
        if remove_original_files_after_download:
            if verbose:
                print("Deleting downloaded file: "+file)
            os.remove(temp_file)

    df = pd.concat(dfs)
    file_name = "mobility-patterns-backfilled_{}_{}".format(
        datetime.strftime(date_start, DATE_FORMATS.DAY),
        datetime.strftime(date_end, DATE_FORMATS.DAY))
    file_name = os.path.join(paths.processed_datasets, file_name)
    path_utils.create_dir_if_necessary(file_name)
    if verbose:
        print("Saving processed file: "+file_name)
    df.to_csv(file_name, encoding='utf-8')

    if return_readed_files:
        return df, readed_files
    return df


download_monthly_patterns_city_data("Houston",
                                    datetime(year=2021, month=2, day=1))
# %%
