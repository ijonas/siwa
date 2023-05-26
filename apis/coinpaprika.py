from apis.crypto_api import CryptoAPI
import requests
from apis import utils


class CoinPaprikaAPI(CryptoAPI):
    def __init__(self):
        self.ohlc_url = "https://api.coinpaprika.com/v1/coins/{coin_id}/ohlcv/latest"  # noqa E501
        super().__init__(
            url="https://api.coinpaprika.com/v1/coins",
            source='coinpaprika'
        )

    @utils.handle_request_errors
    def get_data(self, N):
        response = requests.get(self.url)
        data = response.json()
        # Sorting the coins by market cap
        filtered_data = [coin for coin in data if coin['rank'] != 0]
        sorted_data = sorted(filtered_data, key=lambda coin: coin['rank'])[:N]
        return sorted_data

    @utils.handle_request_errors
    def extract_market_cap(self, data):
        # Fetch the details of each coin
        md = {}
        market_data = {}
        for coin in data:
            coin_id = coin["id"]
            coin_info_url = self.ohlc_url.format(coin_id=coin_id)
            coin_info = requests.get(coin_info_url).json()
            name = coin["name"]
            last_updated = 0  # Updated every 5 mins as per docs: https://api.coinpaprika.com/#tag/Coins/paths/~1coins~1%7Bcoin_id%7D~1ohlcv~1today~1/get # noqa E501
            market_cap = coin_info[0]['market_cap']
            md["name"] = name
            md["last_updated"] = last_updated
            market_data[market_cap] = md

        return market_data
