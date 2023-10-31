from web3 import Web3
from rpcs import get_rpc_urls


class EVM_API:
    def __init__(self, rpc_urls):
        self.web3 = None
        for url in rpc_urls:
            try:
                web3_instance = Web3(Web3.HTTPProvider(url))
                if web3_instance.isConnected():
                    self.web3 = web3_instance
                    break
            except Exception as e:
                print(f"Failed to connect to {url}: {e}")

        if not self.web3:
            raise ConnectionError(
                "Unable to connect to any of the provided RPC URLs."
            )


if __name__ == "__main__":
    rpcs = get_rpc_urls('arbitrum_one')
    RPC_URLS = rpcs.values()
    evm_api = EVM_API(RPC_URLS)
    breakpoint()
