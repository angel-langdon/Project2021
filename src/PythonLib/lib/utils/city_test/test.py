#%%

import pandas as pd

dtypes = {"placekey":"object", "safegraph_place_id":"object", "parent_placekey":"object", "parent_safegraph_place_id":"object",
"location_name":"category", "street_address":"category", "city":"category", "region":"category", "postal_code":"int32",
"safegraph_brand_ids":"object", "brands":"category", "date_range_start":"object", "date_range_end":"object"}

df = pd.read_csv('PATH', dtype=dtypes, encoding='utf-8') #csv name: mobility-patterns-backfilled_2020-01-01_2021-04-13.csv

df.head()
#%%
cadenas = ["Chick-fil-A", 'Shake Shack', 'Five Guys', "Wendy's", "KFC", "Burger King", "Popeyes Louisiana Kitchen", "Subway", "Pizza Hut", "Taco Bell", "Starbucks", "Domino's Pizza", "7-Eleven"]
for cad in cadenas:
    data = df[df['brands'] == cad]
    print(cad, len(set(data['safegraph_place_id']))) #Para saber cuántas tiendas hay en Houston de cada cadena.

#%%

len(set(data['safegraph_place_id']))
# %%

lats = list(set(data['latitude']))
lons = []

for lat in lats:
    dt = pd.DataFrame(data[data['latitude'] == lat])
    dt.head()
    lons.append(dt['longitude'])
    
lons = [float(lon) for fon in lons]

# %%
data = df[df['brands'] == 'Subway'] #filtrado

data.to_csv('Subway_Houston.csv', index = False)
# %%
