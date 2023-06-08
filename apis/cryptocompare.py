from typing import Any, Dict
from apis.crypto_api import CryptoAPI
import requests
from apis import utils
from apis.utils import MissingDataException


class CryptoCompareAPI(CryptoAPI):
    """
    Class to interact with the CryptoCompare API.

    Inherits from:
        CryptoAPI: Parent class to provide a common interface for all crypto APIs.

    Methods:
        get_data(N: int) -> Dict[str, Any]:
            Gets data from CryptoCompare API.
        extract_market_cap(data: Dict[str, Any]) -> Dict[float, Dict[str, str]]:
            Extracts market cap data from API response.
    """

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes for the CryptoCompareAPI object.
        """
        super().__init__(
            url="https://min-api.cryptocompare.com/data/top/mktcapfull",
            source='cryptocompare'
        )

    @utils.handle_request_errors
    def get_data(self, N: int, buffer: int = 2) -> Dict[str, Any]:
        """
        Gets data from CryptoCompare API.

        Parameters:
            N (int):
                Number of cryptocurrencies to fetch.
            buffer (int):
                Number of extra cryptocurrencies to fetch.
                CryptoCompare API sometimes returns coins without RAW data
                (ie, without market cap). This parameter is used to fetch
                extra coins to compensate for this.

        Returns:
            Dict[str, Any]: A dictionary with data fetched from API.
        """
        parameters = {
            "limit": N + buffer,
            "tsym": "USD",
        }
        response = requests.get(self.url, params=parameters)
        if response.status_code == 200:
            data = response.json()
        else:
            raise requests.exceptions.RequestException(
                f"Received status code {response.status_code} "
                f"for URL: {self.url}"
            )
        missing_count = 0
        for coin in data["Data"]:
            try:
                _ = coin["RAW"]
            except KeyError:
                missing_count += 1
                if missing_count > buffer:
                    raise MissingDataException(
                        f"Received {missing_count} coins without RAW data "
                        f"for URL: {self.url}"
                    )
                data["Data"].remove(coin)
        return data['Data'][:N]

    def extract_market_cap(self, data: Dict[str, Any]) -> Dict[float, Dict[str, str]]:
        """
        Extracts market cap data from API response.

        Parameters:
            data (Dict[str, Any]): Data received from API.

        Returns:
            Dict[float, Dict[str, str]]:
                A dictionary with market cap as keys and coin details as values.
        """
        market_data = {}
        for coin in data:
            name = coin["CoinInfo"]["Name"]
            last_updated = coin["RAW"]["USD"]["LASTUPDATE"]
            market_cap = coin["RAW"]["USD"]["MKTCAP"]
            market_data[market_cap] = {
                "name": name,
                "last_updated": last_updated,
            }
        return market_data
