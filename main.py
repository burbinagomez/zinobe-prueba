"""This script run the principal code"""
from config import con
import pandas as pd
import requests
import hashlib
import json
import time



def encrypt(msg):
    """
    This method receive a dict and return a series with encrypt message and time elapsed
    """
    t_s = time.time()
    h = hashlib.sha1()
    h.update(json.dumps(msg).encode("utf-8"))
    return pd.Series((h.hexdigest(),time.time()-t_s))

def get_countries():
    """
    This method call the api from rest countries and return a df with Region, city name, languaje and time
    """
    countries = requests.get("https://restcountries.com/v3.1/all").json()
    keys = countries[0].keys()
    df = pd.DataFrame(countries)
    df["Region"] = df["region"]
    df["City Name"] = df.apply(lambda x: x["name"]["official"],axis=1)
    df[["Languaje","Time"]] = df.apply(lambda x: encrypt(x["languages"]),axis=1)
    df = df.drop(columns=keys)
    return df

def save_sqlite(df):
    """
    This method receive a df and save that in a sqlite file
    """
    try:
        df.to_sql("results",con)
    except Exception as e:
        print(e)

def to_json(df):
    """
    This method receive a df and save that in a json file
    """
    df.to_json(path_or_buf="data.json",orient="records")

def get_info_time_elapsed(df):
    """
    This method recieve a df and print all the information about the time elapsed
    """
    print(f""" Time of execution
    Total: {sum(df['Time'])} s
    Average: {df['Time'].mean()} s
    Min: {df['Time'].min()} s
    Max: {df['Time'].max()} s
    """)

if __name__ == "__main__":
    """
    Run the project
    """
    df = get_countries()
    save_sqlite(df)
    to_json(df)
    get_info_time_elapsed(df)

