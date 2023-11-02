from web3 import Web3
import json
from typing import List, Any
try:
    from apis.evm.rpcs import get_rpc_urls
except ModuleNotFoundError:
    from rpcs import get_rpc_urls


class EVM_API:
    def __init__(self,
                 rpc_urls: List[str],
                 contract_addr: str = None,
                 function_name: str = None,
                 args: List[Any] = None,
                 connect: bool = False,
                 ):
        self.web3 = None
        self.connected = False
        if connect:
            self.connect(rpc_urls)
        if contract_addr is None:
            return
        if contract_addr is not None and function_name is None:
            raise Exception("Must provide function name if contract address "
                            "is provided.")
        self.contract_addr = contract_addr
        self.abi = self.get_abi_from_file(contract_addr)
        self.function_name = function_name
        self.args = args
        self.rpc_urls = rpc_urls

    def get_abi_from_file(self, addr):
        with open(f'apis/evm/abis/{addr}.json') as f:
            return json.load(f)

    def get_values(self, connect_every_time: bool = False):
        # If connect_every_time is True, connect to a provider when this method
        # is called. Also connect if not connected yet.
        if connect_every_time or not self.connected:
            self.connect(self.rpc_urls)
        # Instantiate contract
        contract = self.web3.eth.contract(address=self.contract_addr,
                                          abi=self.abi)
        try:
            # Call function
            func = getattr(contract.functions, self.function_name)
            result = func(*self.args).call()
            return result
        except (AttributeError, TypeError, ValueError) as e:
            raise Exception(
                f"Error calling function {self.function_name} on "
                f"contract {self.contract_addr}: {e}"
            )

    def connect(self, rpc_urls):
        print('Connecting to network...')
        for url in rpc_urls:
            try:
                web3_instance = Web3(Web3.HTTPProvider(url))
                if web3_instance.isConnected():
                    self.web3 = web3_instance
                    self.connected = True
                    break
            except Exception as e:
                print(f"Failed to connect to {url}: {e}")

        if not self.web3:
            raise ConnectionError(
                "Unable to connect to any of the provided RPC URLs."
            )


if __name__ == "__main__":
    rpcs = get_rpc_urls('arbitrum_one')
    rpcs = rpcs.values()
    evm_api = EVM_API(
        '0x4305C4Bc521B052F17d389c2Fe9d37caBeB70d54',
        'balanceOf',
        ['0x33659282d39E62B62060c3F9Fb2230E97db15F1E'],
        rpcs)
    value = evm_api.get_values()
    print(value)
