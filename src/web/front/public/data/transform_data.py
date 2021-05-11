# %%
import os
from datetime import timedelta

import pandas as pd


# %%
def read_csv_data(fname):
    df: pd.DataFrame = pd.read_csv(fname)
    columns = [col for col in df.columns if col != "index"]
    df = df[columns]
    df = df.drop(columns=["visits"])
    df = df.rename(columns={"visits_predicted": "prediction",
                            "old_visits": "visits",
                            "safegraph_place_id": "placekey"})
    df["date"] = pd.to_datetime(df["date"])
    df["prediction"] = df["prediction"].astype(int)
    df = df.dropna(subset=["placekey", "date", "visits", "prediction"])
    return df


# %%

for f in os.scandir('.'):
    if f.name.endswith(".csv"):
        df = read_csv_data(f.name)
        df = df[df["date"] > (df["date"].max() - timedelta(days=31))]
        df.to_json(f.name.replace(".csv", ".json"), "records", indent=4)

# %%
