import requests
from apis import utils


def fetch_data_by_mcap(N):
    assert N <= 250, "Coingecko error: Max output is 250 per page."
    url = "https://api.coingecko.com/api/v3/coins/markets"
    parameters = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": N,
        "page": 1,
        "sparkline": False,
    }

    try:
        response = requests.get(url, params=parameters)
        data = response.json()

        # Extract market cap information from the response
        md = {}
        market_data = {}
        for coin in data:
            name = coin["name"]
            last_updated = coin["last_updated"]
            market_cap = coin["market_cap"]
            md["name"] = name
            md["last_updated"] = last_updated
            market_data[market_cap] = md

        # Store market data in the database
        utils.create_market_cap_database()
        utils.store_market_cap_data(
            market_data=market_data, source='coingecko'
        )

    except requests.exceptions.RequestException as e:
        print("Error occurred while making the API request:", str(e))
        print("Warning: Continuing with the rest of the execution.")
        return None

    return market_data


if __name__ == '__main__':
    fetch_data_by_mcap(10)
