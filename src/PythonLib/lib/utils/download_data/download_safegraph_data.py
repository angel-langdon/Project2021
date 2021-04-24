# %%
import os
import traceback
from datetime import datetime

import boto3
import pandas as pd
from utils.date_utils.date_formats import DATE_FORMATS
from utils.download_data import data_dtypes as dtypes
from utils.file_utils import file_type, file_utils
from utils.path_utils import path_utils, paths
from utils.secrets.secrets import (SAFEGRAPH_ACCESS_KEY_ID, SAFEGRAPH_BUCKET,
                                   SAFEGRAPH_ENDPOINT_URL,
                                   SAFEGRAPH_REGION_NAME,
                                   SAFEGRAPH_SECRET_ACCESS_KEY,
                                   SAFEGRAPH_SERVICE_NAME)


# %%
class SafeGraphSession():
    def __init__(self, prefix, bucket_name, verbose=True):
        self.access_key_id = SAFEGRAPH_ACCESS_KEY_ID
        self.secret_access_key = SAFEGRAPH_SECRET_ACCESS_KEY
        self.service_name = SAFEGRAPH_SERVICE_NAME
        self.bucket_name = SAFEGRAPH_BUCKET
        self.endpoint = SAFEGRAPH_ENDPOINT_URL
        self.region_name = SAFEGRAPH_REGION_NAME
        self.prefix = prefix
        self.verbose = True
        self.all_files = None
        self.files_filtered_by_month = None
        self.files_filtered_by_hour = None

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
        def to_dataframe(date_dict):
            rows = [{"date": datetime.strptime(key, "%Y-%m"),
                     "files": value}
                    for key, value in date_dict.items()]
            return pd.DataFrame(rows)

        if self.files_filtered_by_month:
            if as_dataframe and not isinstance(self.files_filtered_by_month, pd.DataFrame):
                return to_dataframe(self.files_filtered_by_month)
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
        if as_dataframe:
            return to_dataframe(date_dict)
        return self.files_filtered_by_month

    def filter_files_by_hour(self):
        if not self.all_files:
            self.list_all_files()
        date_format = "%Y/%m/%d/%H"
        if self.files_filtered_by_hour is not None:
            return self.files_filtered_by_hour
        rows = []
        for file in self.all_files:
            date_str = "/".join(file.split("/")[2:6])
            date = datetime.strptime(date_str, date_format)
            f_type = file_type.get_file_type(file)
            row = {"date": date, "file": file, "type": f_type}
            rows.append(row)
        self.files_filtered_by_hour = pd.DataFrame(rows)
        return self.files_filtered_by_hour

    def download_file(self, bucket_path: str, dest_path: str = None,
                      append_datasets_path: bool = True):
        if not dest_path:
            dest_path = bucket_path
        if append_datasets_path:
            dest_path = os.path.join(paths.DATASETS, dest_path)
        if not os.path.isfile(dest_path):
            path_utils.create_dir_if_necessary(dest_path)

            if self.verbose:
                print(f"Saving file in: {dest_path}")
            self.client.download_file(self.bucket_name,
                                      bucket_path, dest_path)
        else:
            if self.verbose:
                print("File already exists:", dest_path)
        return dest_path


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
                                        verbose: bool = True,
                                        target_region=None):
    """
    Downloads montly patterns data given a target city and a 
    window of time

    >>> download_monthly_patterns_city_data("Houston",
                                            datetime(year=2021, month=3, day=1),
                                            remove_original_files_after_download=False)
    """
    def get_file_name(date_start, date_end, target_city):
        file_name = "{}/mobility-patterns-backfilled_{}_{}.csv".format(
            target_city,
            datetime.strftime(date_start, DATE_FORMATS.DAY),
            datetime.strftime(date_end, DATE_FORMATS.DAY))
        file_name = os.path.join(paths.processed_datasets, file_name)
        return file_name

    if not date_end:
        # if no date_end is passed it infers to have the most recent data
        date_end = datetime.now()

    file_name = get_file_name(date_start, date_end, target_city)
    # In case the file exists return it

    if os.path.isfile(file_name):
        if verbose:
            print("File already exists:", file_name)
        return pd.read_csv(file_name, encoding="utf8")
    prefix = 'monthly-patterns-2020-12'
    bucket = "sg-c19-response"
    session = SafeGraphSession(prefix, bucket)
    df = session.filter_files_by_month(as_dataframe=True)

    df = df[(df["date"] >= date_start) & (df["date"] <= date_end)]
    files = [f for f in df.explode("files")["files"]
             if file_type.is_mobility_pattern(f)]
    dfs = []
    try:
        for i, file in enumerate(files):
            temp_file = os.path.join(paths.temp_datasets, file)
            session.download_file(file, temp_file)
            # read the file in chunks filter it and store in a list of dataframes
            if verbose:
                print("Reading: "+file)
            for chunk in pd.read_csv(temp_file,
                                     encoding="utf-8",
                                     sep=",",
                                     chunksize=10000,
                                     dtype=dtypes.mobility_dtypes):
                if target_region:
                    filtered = chunk[(chunk["city"] == target_city) &
                                     (chunk["region"] == target_region)].copy()
                else:
                    filtered = chunk[chunk["city"] == target_city]
                dfs.append(filtered)

            # once readed delete the file to free memmory
            if remove_original_files_after_download:
                if verbose:
                    print("Deleting downloaded file: "+file)
                os.remove(temp_file)

        df = pd.concat(dfs)

        path_utils.create_dir_if_necessary(file_name)
        if verbose:
            print("Saving processed file: "+file_name)
        df.to_csv(file_name, encoding='utf-8', index=False)

        return df
    except:
        # Print the exception
        traceback.print_exc()
        # In case anything fails return the current filtered data
        # the files and the current downloaded file
        return dfs, files, i


# res = download_monthly_patterns_city_data("Houston",
#                                          datetime(year=2020, month=1, day=1),
#                                          remove_original_files_after_download=True)
def download_core_poi():
    prefix = 'core-places-delivery'
    bucket = "sg-c19-response"
    session = SafeGraphSession(prefix, bucket)
    df_files = session.filter_files_by_hour()
    recent_files_to_download = []
    for _, group in df_files.groupby(by="type"):
        group = group.sort_values(by="date")
        most_recent_date = group["date"].iloc[-1]
        group = group[group["date"] == most_recent_date]
        recent_files_to_download.extend(group["file"])
    for file in recent_files_to_download:
        session.download_file(file)
# %%


def download_lastest_home_pannel_summary():
    prefix = 'monthly-patterns'
    bucket = "sg-c19-response"
    session = SafeGraphSession(prefix, bucket)
    df = session.filter_files_by_hour()
    df = df[df["type"] == "home_panel_summary"]
    df = df.sort_values("date", ascending=False)
    file_path = df["file"].iloc[0]
    return session.download_file(file_path)


# %%


# %%
