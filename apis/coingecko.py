from typing import Any, Dict
from apis.crypto_api import CryptoAPI
import requests
from apis import utils


class CoinGeckoAPI(CryptoAPI):
    """
    Class to interact with the CoinGecko API.

    Inherits from:
        CryptoAPI: Parent class to provide a common interface for all crypto APIs.

    Methods:
        get_data(N: int) -> Dict[str, Any]:
            Gets data from CoinGecko API.
        extract_market_cap(data: Dict[str, Any]) -> Dict[float, Dict[str, str]]:
            Extracts market cap data from API response.
    """
    
    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the CoinGeckoAPI object.
        """
        super().__init__(
            url="https://api.coingecko.com/api/v3/coins/markets",
            source='coingecko'
        )

    @utils.handle_request_errors
    def get_data(self, N: int) -> Dict[str, Any]:
        """
        Gets data from CoinGecko API.

        Parameters:
            N (int): Number of cryptocurrencies to fetch.

        Returns:
            Dict[str, Any]: A dictionary with data fetched from API.
        """
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
        for coin in data:
            name = coin["name"]
            last_updated = coin["last_updated"]
            market_cap = coin["market_cap"]
            md["name"] = name
            md["last_updated"] = last_updated
            market_data[market_cap] = md
        return market_data
