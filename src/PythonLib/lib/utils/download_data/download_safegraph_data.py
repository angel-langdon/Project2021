# %%
import sys

import boto3
import numpy as np
import pandas as pd
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

        self.session = boto3.Session(
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region_name)
        self.client = self.session.client(self.service_name,
                                          endpoint_url=self.endpoint)
        self.bucket = self.session.resource(self.service_name,
                                            endpoint_url=self.endpoint).Bucket(bucket_name)

    def download_file(self, bucket_path, dest_path):
        self.client.download_file(self.bucket_name, bucket_path, dest_path)


prefix = 'monthly-patterns-2020-12'
bucket = "sg-c19-response"
session = SafeGraphSession(prefix, bucket)
# %%

# lists all relevant objects in the S3 bucket and stores the paths by date in the date_dict
bucket_obj = session.bucket
# %%
files_in_bucket = list(bucket_obj.objects.all())
# %%
print(len(files_in_bucket))
files = [elm.key for elm in files_in_bucket if elm.key.startswith(
    prefix) and (elm.key.endswith('.csv') or elm.key.endswith('.csv.gz'))]
print(len(files))
# %%
session.download_file(files[0], "prueba.csv")
# %%


def filter_files_by_date(files):
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
    return date_dict


res = filter_files_by_date(files)
