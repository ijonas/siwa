from apis.crypto_api import CryptoAPI
import requests
from apis import utils


class CoinMarketCapAPI(CryptoAPI):
    def __init__(self):
        super().__init__(
            url="https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",  # noqa
            source='coinmarketcap'
        )
        self.headers = {
            "X-CMC_PRO_API_KEY": utils.get_api_key('coinmarketcap'),
        }

    @utils.handle_request_errors
    def get_data(self, N):
        parameters = {
            "limit": N
        }
        response = requests.get(
            self.url, headers=self.headers, params=parameters
        )
        data = response.json()
        return data

    def extract_market_cap(self, data):
        md = {}
        market_data = {}
        for coin in data["data"]:
            name = coin["name"]
            last_updated = coin["last_updated"]
            market_cap = coin["quote"]["USD"]["market_cap"]
            md["name"] = name
            md["last_updated"] = last_updated
            market_data[market_cap] = md
        return market_data
