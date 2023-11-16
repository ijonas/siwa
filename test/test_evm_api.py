# test_evm_api.py
import unittest
from unittest.mock import patch, MagicMock
from apis.evm import evm_api


class TestEVM_API(unittest.TestCase):
    @patch('apis.evm.evm_api.Web3')
    def setUp(self, MockWeb3):
        # Mock the Web3 instance
        self.mock_web3 = MockWeb3()
        self.mock_web3.eth.contract.return_value = MagicMock()
        self.evm_api = evm_api.EVM_API(
            rpc_urls=['http://mocked_rpc_url'],
            contract_addr='0xMockedContractAddress',
            function_name='balanceOf',
            args=['0xMockedAddress'],
            connect=True
        )
        self.evm_api.web3 = self.mock_web3

    @patch('apis.evm.evm_api.open', new_callable=unittest.mock.mock_open,
           read_data='{"abi": true}')
    def test_get_abi_from_file(self, mock_file):
        # Test if ABI is loaded correctly from file
        abi = self.evm_api.get_abi_from_file('0xMockedContractAddress')
        self.assertTrue(abi)
        mock_file.assert_called_with('apis/evm/abis/0xMockedContractAddress.json')

    def test_get_values(self):
        # Test the get_values method
        self.mock_web3\
            .eth.contract.return_value.functions.balanceOf.return_value.call\
                .return_value = 1000
        result = self.evm_api.get_values()
        self.assertEqual(result, 1000)


if __name__ == '__main__':
    unittest.main()
