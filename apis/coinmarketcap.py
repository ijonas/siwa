import requests
import json
import os


def get_api_key():
    if not os.path.exists("apis/api_keys.json"):
        print('Create a file called "api_keys.json" in the "apis"'
              'directory and add your coinmarketcap api key to it.')
        raise Exception("api_keys.json not found")
    with open("apis/api_keys.json", "r") as f:
        api_keys = json.load(f)
        return api_keys["coinmarketcap"]


def fetch_data_by_mcap(N):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        "limit": N,
    }

    headers = {
        "X-CMC_PRO_API_KEY": get_api_key(),
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()

    # Extract market cap information from the response
    market_data = {}
    for coin in data["data"]:
        name = coin["name"]
        market_cap = coin["quote"]["USD"]["market_cap"]
        market_data[market_cap] = name
    return market_data


if __name__ == '__main__':
    fetch_data_by_mcap(10)