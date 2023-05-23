'''
    === OVERLAY INDEX BUILDER ===
    This program will:
    * fetch CoinGecko market data
    * apply weighting algorithm to data
    * store data in SQLite database
    * push data to airnode [NOT IMPLEMENTED]
    * do all of the above in a loop if required

    in this codebase, "market_data" will be a dict of dicts
        key is market id
        value corresponds to database columns per overlay_dbsetup.py

    e.g.:
    market_data = {
        'bitcoin':{'symbol':'btc', 'id':'bitcoin','market_cap':468816620783, ... },
        'ethereum':{'symbol':'eth', 'id':'ethereum','market_cap':168816620783, ... },
        }

'''

# standard library:
import sqlite3, json, time, datetime, traceback

# third party libraries:
import requests

from apis import utils

def convert_data_list_to_market_id_dict(raw_data):
    """convert python's JSON-list-of-dicts to dict-of-dicts where dict key is market ID
    so that instead of jlist[0]['last_updated'] we can say jlist['bitcoin']['last_updated'] etc"""
    return {d['id']:d for d in raw_data}

def convert_data_list_to_mcap_dict(raw_data):
    """convert python's JSON-list-of-dicts to dict-of-dicts where dict key is marcket cap
    so that instead of jlist[0]['last_updated'] we can say jlist['bitcoin']['last_updated'] etc"""
    return {d['market_cap']:d for d in raw_data}

def fetch_data_from_disk(market_ids, filename="test_data.json"):
    """load JSON data from disk for given market ids
    mostly for debugging, offline work, unit tests, etc;
    returns list of dicts, one dict per market id"""

    with open(filename) as file:
        raw_data = list()
        json_data = json.load(file)
        for row in json_data:
            if row['id'] in market_ids:
                row['last_updated_unixtime'] = utils.convert_timestamp_to_unixtime(row['last_updated'])
                raw_data.append(row)
            market_data = convert_data_list_to_market_id_dict(raw_data)
        return market_data


def fetch_data_by_mcap(N):
    """load JSON data from web for top N market caps
    returns list of dicts, one dict per market id"""

    per_page = 250 # max allowed by API is 250
    pages = N // per_page + 1
    market_data = dict()
    try:
        for page in range(1, pages + 1):
            coingecko_url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={per_page}&page={page}'
            # coingecko_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={market_ids}"
            response = requests.get(coingecko_url)
            raw_data = response.json()
            for row in raw_data:
                row['last_updated_unixtime'] = utils.convert_timestamp_to_unixtime(row['last_updated'])
            market_data.update(convert_data_list_to_mcap_dict(raw_data))

    except Exception as e:
        #NOTE: Exceptions might be thrown here for several reasons,
        # for example ratelimiting, network outages, etc
        print('CoinGecko Error: ', e)
        print('Traceback: ', traceback.format_exc())
        return None

    return market_data

def fetch_markets():
    """fetches JSON data from coingecko API for a list of market ids
    returns list of dicts, one dict per market id"""

    coingecko_url = f"https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(coingecko_url)
    raw_data = response.json()
    breakpoint()

def fetch_data_from_web(market_ids):
    """fetches JSON data from coingecko API for a list of market ids
    returns list of dicts, one dict per market id"""
    try:
        market_ids = ','.join(market_ids)
        coingecko_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={market_ids}"
        response = requests.get(coingecko_url)
        raw_data = response.json()
        for row in raw_data:
            row['last_updated_unixtime'] = utils.convert_timestamp_to_unixtime(row['last_updated'])
        market_data = convert_data_list_to_market_id_dict(raw_data)
        return market_data

    except Exception as e:
        #NOTE: Exceptions might be thrown here for several reasons,
        # for example ratelimiting, network outages, etc
        print('CoinGecko Error: ', e)
        print('Traceback: ', traceback.format_exc())
        return None


def dict_factory(cursor, row):
    """sqlite3 row_factory returns db results as python dicts for convenience"""
    return {col[0]:row[idx] for idx,col in enumerate(cursor.description)}


def fetch_most_recent_data_from_db(market_ids):
    """fetch most recent data from database for given market ids,
    returns list of dicts, one dict per id"""

    #connect to db with python timestamp parsing enabled
    conn = sqlite3.connect("overlay_indices.db")
    conn.row_factory = dict_factory

    cur = conn.cursor()
    raw_data = cur.execute('''
                SELECT *, MAX(last_updated_unixtime) as last_updated_unixtime
                FROM data GROUP BY id''').fetchall()
    conn.close()
    market_data = convert_data_list_to_market_id_dict(raw_data)
    return market_data


def store_data(processed_data):
    """stores coingecko API data in sqlite database"""
    conn = sqlite3.connect("overlay_indices.db")
    cur = conn.cursor()

    #store a row in the db for each market fetched
    for market in processed_data.values():
        # list keys explicitly for clarity
        # also prevents accidentally trying to add keys for cols that dont exist in DB
        # if coingecko updates their API to start including extra data
        keys = ['id', 'symbol', 'name', 'current_price', 'market_cap', 'market_cap_rank',
        'fully_diluted_valuation', 'total_volume', 'high_24h', 'low_24h', 'price_change_24h',
        'price_change_percentage_24h', 'market_cap_change_24h', 'market_cap_change_percentage_24h',
        'circulating_supply', 'total_supply', 'max_supply', 'ath', 'ath_change_percentage',
        'ath_date', 'atl', 'atl_change_percentage', 'atl_date', 'last_updated',
        #keys below here are our own, i.e. not directly from the coingecko API
        'last_updated_unixtime', 'weighted_value', 'weighting_algorithm_version']
        values = [market[k] for k in keys]

        key_string = ','.join(keys)
        insert_string = ','.join(['?' for n in range(len(values))])
        cur.execute(f'''INSERT INTO data ({key_string})
                        VALUES ({insert_string})''', (values))

    conn.commit()
    conn.close()
    return True


def process_data(market_data):
    """applies weighting algorithm,
    returns list dicts, one per market id, but with additional 'weighted_val' column

    Description of current algorithm:
        * Weight each market according to its percentage of bitcoin's market cap
    """

    # NOTE: we keep track of when this function was modified in the algorithm_version var
    # this will tell us how a particular weighted_value was arrived at if we
    # in the future modify the weighting algorithm, but want to keep unmodified
    # historical records instead of retroactively re-weighting things.

    # TODO: INCREMENT THIS VERSION NUMBER IF YOU ALTER THIS FUNCTION ***
    # NOTE: (alternatively, we could automatically use the hash of this function
    #       instead of incrementing a version number)

    algorithm_version = 1
    bitcoin_market_cap = market_data['bitcoin']['market_cap']

    for market in market_data:
        weighted_value = market_data[market]['market_cap'] / bitcoin_market_cap

        market_data[market]['weighted_value'] = weighted_value
        market_data[market]['weighting_algorithm_version'] = algorithm_version

    return market_data


def push_data(market_data):
    """pushes data to airnode"""
    pass


def poll_loop(market_ids, delay=60, iterations=-1):
    """fetch, store, process, and push data regularly

    ::: Parameters :::
    delay -- how often to run loop (in seconds), i.e. every 60 seconds
    iterations -- number of iterations, or -1 to run forever
    """

    loop_count = 1 # loop iteration we are currently on
    while True:
        print(f"\n\t\t##### starting loop {loop_count} of {iterations} #####\n")

        print(':: fetching data from CoinGecko API ')
        market_data = fetch_data_from_web(market_ids)
        #or, for testing and debugging:
        #market_data = fetch_data_from_disk(market_ids)

        #check data exists / there was no network or API error:
        if market_data != None:
            print(':: processing / weighting data ')
            processed_data = process_data(market_data)

            print(':: storing data in SQLite database')
            store_data(processed_data)

            print(':: pushing data to Airnode [NOT IMPLEMENTED]\n')
            push_data(processed_data)

        else:
            #TODO: notify someone here?
            #i.e. detect error type, notify someone that
            #we have a network outage, API error, etc
            pass

        ### wait for API ratelimit or end loop if finite iterations specified ###
        loop_count += 1

        # check if we're finished (if not in -1 infinite loop mode)
        if loop_count > iterations:
            print(f'\n--> Polling complete. ({iterations} iterations)\n')
            break

        # check if okay to query API again [ratelimiting]
        for second in range(delay):
            if second%5==0:
                print(f"[ratelimiting @ {datetime.datetime.now().strftime('%H:%M:%S')}] "+\
                         f"Next API request in {delay-second} seconds")
            time.sleep(1)


if __name__ == "__main__":
    #which markets we want to fetch
    market_ids = ["bitcoin", "ethereum", "litecoin"]

    #poll coingecko API once a minute for 10 minutes:
    # poll_loop(market_ids, iterations = 10, delay = 6)

    #or poll coingecko API forever:
    # poll_loop(market_ids, iterations = -1, delay=60) #loop forever
    markets = fetch_data_by_mcap(1000)
    breakpoint()
