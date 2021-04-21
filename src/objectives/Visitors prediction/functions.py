import json
import os
from datetime import datetime, timedelta

import holidays
import pandas as pd


def is_weekend(df):
    df['date'] = pd.to_datetime(df['date']) 

    df['is_weekend'] = df['date'].dt.day_name()
    df.loc[df['is_weekend'] == "Saturday", 'is_weekend'] = 1
    df.loc[df['is_weekend'] == "Sunday", 'is_weekend'] = 1
    df.loc[df['is_weekend'] == "Monday", 'is_weekend'] = 0
    df.loc[df['is_weekend'] == "Tuesday", 'is_weekend'] = 0
    df.loc[df['is_weekend'] == "Wednesday", 'is_weekend'] = 0
    df.loc[df['is_weekend'] == "Thursday", 'is_weekend'] = 0
    df.loc[df['is_weekend'] == "Friday", 'is_weekend'] = 0

    return df

def is_holiday(df):
    holi = holidays.CountryHoliday('US', prov="Houston", state='TX')
    df["is_holiday"] = [1 if d in holi else 0 for d in df["date"]]
    return df

def last_day(df):
    stores = set(df['placekey'])
    i = 0
    for store in stores:
        new = df[df['placekey'] == store]
        l = []
        
        #for row in new.iterrows():
        yesterday = new['date'] - timedelta(days = 1)
        yesterday = yesterday.dt.strftime('%Y-%m-%d')
        set_raro = set(new['date'].dt.strftime('%Y-%m-%d'))
        for day in yesterday:
            if day in set_raro:
                visits = list(new[new['date'] == day]['visits'])
                l.append(visits[0])
                
            else:
                l.append(0)
        
        new['visits_last_day'] = l

        if i == 0:
            old = new
            i += 1
        else:
            old = pd.concat([old, new])
    return old

def last_week(df):
    stores = set(df['placekey'])
    i = 0
    for store in stores:
        new = df[df['placekey'] == store]
        l = []
        
        #for row in new.iterrows():
        yesterday = new['date'] - timedelta(days = 7)
        yesterday = yesterday.dt.strftime('%Y-%m-%d')
        set_raro = set(new['date'].dt.strftime('%Y-%m-%d'))
        for day in yesterday:
            if day in set_raro:
                visits = list(new[new['date'] == day]['visits'])
                l.append(visits[0])
                
            else:
                l.append(0)
        
        new['visits_last_week'] = l

        if i == 0:
            old = new
            i += 1
        else:
            old = pd.concat([old, new])
    return old

"""
subway = pd.read_csv('Subway_Houston_days.csv', encoding="utf-8") #Needed to filter by state TX.
subway = is_weekend(subway)
subway = is_holiday(subway)
subway = last_day(subway)
subway = last_week(subway)
"""
