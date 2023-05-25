import requests
from apis import utils


def fetch_data_by_mcap(N):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        "limit": N,
    }

    headers = {
        "X-CMC_PRO_API_KEY": utils.get_api_key('coinmarketcap'),
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()

        # Extract market cap information from the response
        md = {}
        market_data = {}
        for coin in data["data"]:
            name = coin["name"]
            last_updated = coin["last_updated"]
            market_cap = coin["quote"]["USD"]["market_cap"]
            md["name"] = name
            md["last_updated"] = last_updated
            market_data[market_cap] = md

        # Store market data in the database
        utils.create_market_cap_database()
        utils.store_market_cap_data(
            market_data=market_data, source='coinmarketcap'
        )

    except requests.exceptions.RequestException as e:
        print("Error occurred while making the API request:", str(e))
        print("Warning: Continuing with the rest of the execution.")
        return None

    return market_data


if __name__ == '__main__':
    fetch_data_by_mcap(10)
