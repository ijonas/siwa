from web3 import Web3


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
    RPC_URLS = [
        "https://arbitrum-one.gateway.pokt.network/v1/lb/a609ace3fe0c00927e127927"
    ]
    evm_api = EVM_API(RPC_URLS)
    breakpoint()
