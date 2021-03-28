# %%
import boto3
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

# %%

""" Download geometry data

"""
