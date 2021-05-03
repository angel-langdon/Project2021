# %%
from datetime import timedelta

import pandas as pd


# %%
def read_csv_data():
    df = pd.read_csv("data.csv")
    columns = [col for col in df.columns if col != "index"]
    df = df[columns]
    df["date"] = pd.to_datetime(df["date"])
    df["prediciton"] = df["prediction"].astype(int)
    return df


df = read_csv_data()
df = df[df["date"] > (df["date"].max() - timedelta(days=31))]
# %%
