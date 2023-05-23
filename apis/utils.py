import datetime
import sqlite3
import time
import os
import json


def convert_timestamp_to_unixtime(timestamp):
    """takes a timestamp e.g. '2022-08-11T09:10:12.364Z' returns a unix time 1660209012.364"""
    unix_datetime = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
    return unix_datetime.timestamp()


def create_market_cap_database(db_path='data.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS "
        "market_cap_data (name TEXT, market_cap REAL, last_updated_time REAL, load_time REAL, source TEXT)"
    )
    conn.commit()
    conn.close()


def store_market_cap_data(market_data, source, db_path='data.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for market_cap, md in market_data.items():
        cursor.execute(
            "INSERT INTO market_cap_data (name, market_cap, last_updated_time, load_time, source)"
            "VALUES (?, ?, ?, ?, ?)",
            (md['name'], market_cap, md['last_updated'], int(time.time()), source))
    conn.commit()
    conn.close()


def get_api_key(api_provider_name):
    if not os.path.exists("apis/api_keys.json"):
        print('Create a file called "api_keys.json" in the "apis"'
              'directory and add your API keys it.')
        raise Exception("api_keys.json not found")
    with open("apis/api_keys.json", "r") as f:
        api_keys = json.load(f)
        return api_keys[api_provider_name]