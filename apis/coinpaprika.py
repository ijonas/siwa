import requests
from apis import utils


def fetch_data_by_mcap(N):
    url = "https://api.coinpaprika.com/v1/coins"

    try:
        response = requests.get(url)
        data = response.json()

        # Sorting the coins by market cap
        filtered_data = [coin for coin in data if coin['rank'] != 0]
        sorted_data = sorted(filtered_data, key=lambda coin: coin['rank'])[:N]

        # Extract market cap information from the response
        md = {}
        market_data = {}
        for coin in sorted_data:
            coin_id = coin["id"]
            coin_info_url = f"https://api.coinpaprika.com/v1/coins/{coin_id}/ohlcv/today/"  # noqa E501
            coin_info = requests.get(coin_info_url).json()
            name = coin["name"]
            last_updated = 0  # Updated every 5 mins as per docs: https://api.coinpaprika.com/#tag/Coins/paths/~1coins~1%7Bcoin_id%7D~1ohlcv~1today~1/get
            market_cap = coin_info[0]['market_cap']
            md["name"] = name
            md["last_updated"] = last_updated
            market_data[market_cap] = md

        # Store market data in the database
        utils.create_market_cap_database()
        utils.store_market_cap_data(
            market_data=market_data, source='coinpaprika'
        )

    except requests.exceptions.RequestException as e:
        print("Error occurred while making the API request:", str(e))
        print("Warning: Continuing with the rest of the execution.")
        return None

    return market_data


if __name__ == '__main__':
    fetch_data_by_mcap(10)
