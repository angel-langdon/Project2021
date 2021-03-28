# %%
import boto3
from utils.secrets.secrets import (SAFEGRAPH_ACCESS_KEY_ID,
                                   SAFEGRAPH_SECRET_ACCESS_KEY)


# %%
class SafeGrahSession():
    def __init__(self, prefix):
        self.access_key_id = SAFEGRAPH_ACCESS_KEY_ID
        self.secret_access_key = SAFEGRAPH_SECRET_ACCESS_KEY
        self.prefix = prefix


session = boto3.Session(
    aws_access_key_id=SAFEGRAPH_ACCESS_KEY_ID,
    aws_secret_access_key=SAFEGRAPH_SECRET_ACCESS_KEY)

bucket = 'sg-c19-response'
prefix = 'monthly-patterns-2020-12'
s3 = session.client('s3', endpoint_url='https://s3.wasabisys.com')
# %%

# lists all relevant objects in the S3 bucket and stores the paths by date in the date_dict
s3r = session.resource('s3', endpoint_url='https://s3.wasabisys.com')
bucket_obj = s3r.Bucket(bucket)
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
