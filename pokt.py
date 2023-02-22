from dataclasses import dataclass
import constants as c
from numpy import random
from web3 import Web3

#we use Pokt to access chain data
class Pokt():
    '''A class to collect Pokt functionality
    '''

    ARBITRUM = 'https://goerli-rollup.arbitrum.io/rpc' #f'https://{c.POKT_ARBITRUM}.gateway.pokt.network/v1/lb/{c.POKT_PORTAL_ID}'
    ETHEREUM = f'https://{c.POKT_ETHEREUM}.gateway.pokt.network/v1/lb/{c.POKT_PORTAL_ID}'




    A = Web3(Web3.HTTPProvider(ARBITRUM))
    E = Web3(Web3.HTTPProvider(ETHEREUM))

    @staticmethod
    def contract_interface(provider, address, abi):
        return provider.eth.contract(address=address, abi=abi)



class Translucent(Pokt):

    gauss_test  = Pokt.contract_interface(
            Pokt.A,
            address=c.TRANSLUCENT_GAUSS_GOERLI_ARBITRUM,
            abi=c.TRANSLUCENT_FLUX_AGGREGATOR
        )
    gauss_test_E  = Pokt.contract_interface(
            Pokt.E,
            address=c.TRANSLUCENT_GAUSS_GOERLI_ARBITRUM,
            abi=c.TRANSLUCENT_FLUX_AGGREGATOR
        )

