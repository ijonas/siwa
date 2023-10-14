import unittest
import pandas as pd
from unittest.mock import patch, Mock
from apis import csgoskins


class TestCSGOSkins(unittest.TestCase):

    def setUp(self):
        self.csgo = csgoskins.CSGOSkins()

    @patch('requests.request')
    def test_get_prices(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test_data"}
        mock_request.return_value = mock_response

        result = self.csgo.get_prices()

        self.assertEqual(result, {"data": "test_data"})


if __name__ == '__main__':
    unittest.main()
