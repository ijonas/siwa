from typing import Any, Dict
from apis.crypto_api import CryptoAPI
import requests
from apis import utils


class CoinMarketCapAPI(CryptoAPI):
    """
    Class to interact with the CoinMarketCap API.

    Inherits from:
        CryptoAPI: Parent class to provide a common interface for all crypto APIs.

    Methods:
        get_data(N: int) -> Dict[str, Any]:
            Gets data from CoinMarketCap API.
        extract_market_cap(data: Dict[str, Any]) -> Dict[float, Dict[str, str]]:
            Extracts market cap data from API response.
    """
    
    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the CoinMarketCapAPI object.
        """
        super().__init__(
            url="https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",  # noqa
            source='coinmarketcap'
        )
        self.headers = {
            "X-CMC_PRO_API_KEY": utils.get_api_key('coinmarketcap'),
        }

    @utils.handle_request_errors
    def get_data(self, N: int) -> Dict[str, Any]:
        """
        Gets data from CoinMarketCap API.

        Parameters:
            N (int): Number of cryptocurrencies to fetch.

        Returns:
            Dict[str, Any]: A dictionary with data fetched from API.
        """
        parameters = {
            "limit": N
        }
        response = requests.get(
            self.url, headers=self.headers, params=parameters
        )
        data = response.json()
        return data

    def extract_market_cap(self, data: Dict[str, Any]) -> Dict[float, Dict[str, str]]:
        """
        Extracts market cap data from API response.

        Parameters:
            data (Dict[str, Any]): Data received from API.

        Returns:
            Dict[float, Dict[str, str]]:
                A dictionary with market cap as keys and coin details as values.
        """
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
