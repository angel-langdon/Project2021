# %%
import os

import pandas as pd
import plotly.express as px
from utils.download_data import data_dtypes as dtypes
from utils.path_utils import paths

houston_path = os.path.join(paths.processed_datasets,
                            "Houston",
                            "subway.csv")
df = pd.read_csv(houston_path,
                 dtype=dtypes.mobility_dtypes,
                 encoding='utf-8')


lat = df['latitude'].unique()
lon = df['longitude'].unique()
d = {'lat': lat, 'lon': lon}
new = pd.DataFrame(d)

fig = px.scatter_mapbox(new, lat="lat", lon="lon",  zoom=8.3, height=500)
fig.update_layout(mapbox={
    'center': {'lon': new["lon"].mean(), 'lat': new["lat"].mean()},
    'style': "open-street-map"})
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()
