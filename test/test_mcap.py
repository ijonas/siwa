import unittest
from unittest.mock import patch, MagicMock
from apis import crypto_api, coingecko, coinpaprika, coinmarketcap, cryptocompare
from apis import utils


class TestCryptoAPI(unittest.TestCase):
    def setUp(self):
        self.crypto_api = crypto_api.CryptoAPI("https://example.com/api", "example")

    def test_initialization(self):
        self.assertEqual(self.crypto_api.url, "https://example.com/api")
        self.assertEqual(self.crypto_api.source, "example")

    def test_abstract_methods(self):
        self.assertRaises(NotImplementedError, self.crypto_api.get_data, 10)
        self.assertRaises(NotImplementedError, self.crypto_api.extract_market_cap, {})


class TestCoinGeckoAPI(unittest.TestCase):
    def setUp(self):
        self.coin_gecko_api = coingecko.CoinGeckoAPI()

    @patch("requests.get")
    def test_get_data(self, mock_get):
        mock_get.return_value.json.return_value = MagicMock()
        self.coin_gecko_api.get_data(10)
        self.assertTrue(mock_get.called)

    def test_extract_market_cap(self):
        data = [{"name": "Bitcoin", "last_updated": "2023-06-01T10:10:10.000Z", "market_cap": 100000}]
        result = self.coin_gecko_api.extract_market_cap(data)
        self.assertIsInstance(result, dict)
        self.assertEqual(list(result.keys())[0], 100000)


# class TestCoinPaprikaAPI(unittest.TestCase):
#     def setUp(self):
#         self.coin_paprika_api = coinpaprika.CoinPaprikaAPI()

#     @patch("requests.get")
#     def test_get_data(self, mock_get):
#         mock_get.return_value.json.return_value = MagicMock()
#         self.coin_paprika_api.get_data(10)
#         self.assertTrue(mock_get.called)

#     @patch("requests.get")
#     def test_extract_market_cap(self, mock_get):
#         mock_json_return = mock_get.return_value.json
#         mock_json_return.return_value = [{'market_cap': 100000}]
#         mock_get.return_value.status_code = 200
#         data = [{"id": "btc-bitcoin", "name": "Bitcoin", "rank": 1}]
#         result = self.coin_paprika_api.extract_market_cap(data)
#         self.assertIsInstance(result, dict)
#         self.assertEqual([i for i in result][0], 100000)


class TestCoinMarketCapAPI(unittest.TestCase):
    def setUp(self):
        self.coin_market_cap_api = coinmarketcap.CoinMarketCapAPI()

    @patch("requests.get")
    def test_get_data(self, mock_get):
        mock_get.return_value.json.return_value = MagicMock()
        self.coin_market_cap_api.get_data(10)
        self.assertTrue(mock_get.called)

    def test_extract_market_cap(self):
        data = {"data": [{"name": "Bitcoin", "last_updated": "2023-06-01T10:10:10.000Z", "quote": {"USD": {"market_cap": 100000}}}]}
        result = self.coin_market_cap_api.extract_market_cap(data)
        self.assertIsInstance(result, dict)
        self.assertEqual(list(result.keys())[0], 100000)


class TestCryptoCompareAPI(unittest.TestCase):
    def setUp(self):
        self.crypto_compare_api = cryptocompare.CryptoCompareAPI()

    def test_initialization(self):
        self.assertEqual(self.crypto_compare_api.url, "https://min-api.cryptocompare.com/data/top/mktcapfull")
        self.assertEqual(self.crypto_compare_api.source, "cryptocompare")

    @patch("requests.get")
    def test_get_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"Data": [MagicMock()] * 10}
        data = self.crypto_compare_api.get_data(10)
        self.assertTrue(mock_get.called)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 10)

    @patch('requests.get')
    def test_get_data_returns_none_on_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        result = self.crypto_compare_api.get_data(10)
        self.assertIsNone(result)

    def test_extract_market_cap(self):
        data = [{
            "CoinInfo": {"Name": "Bitcoin"},
            "RAW": {"USD":
                    {"LASTUPDATE": "2023-06-01T10:10:10.000Z",
                     "MKTCAP": 100000}}
        }]
        result = self.crypto_compare_api.extract_market_cap(data)
        self.assertIsInstance(result, dict)
        self.assertEqual(list(result.keys())[0], 100000)
        self.assertEqual(result[100000]['name'], 'Bitcoin')
        self.assertEqual(result[100000]['last_updated'],
                         '2023-06-01T10:10:10.000Z')


class TestUtils(unittest.TestCase):
    @patch("datetime.datetime")
    def test_convert_timestamp_to_unixtime(self, mock_datetime):
        utils.convert_timestamp_to_unixtime('2023-06-01T10:10:10.000Z')
        self.assertTrue(mock_datetime.strptime.called)


if __name__ == '__main__':
    unittest.main()
