from apis.crypto_api import CryptoAPI
import requests
from apis import utils


class CoinGeckoAPI(CryptoAPI):
    def __init__(self):
        super().__init__(
            url="https://api.coingecko.com/api/v3/coins/markets",
            source='coingecko'
        )

    @utils.handle_request_errors
    def get_data(self, N):
        parameters = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": N,
            "page": 1,
            "sparkline": False,
        }
        response = requests.get(self.url, params=parameters)
        data = response.json()
        return data

    def extract_market_cap(self, data):
        md = {}
        market_data = {}
        for coin in data:
            name = coin["name"]
            last_updated = coin["last_updated"]
            market_cap = coin["market_cap"]
            md["name"] = name
            md["last_updated"] = last_updated
            market_data[market_cap] = md
        return market_data
