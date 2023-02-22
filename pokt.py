from dataclasses import dataclass
import constants as c
from numpy import random
from web3 import Web3



arbi_goerli = Web3(Web3.HTTPProvider(c.ARBITRUM_GOERLI))
arbi_main = Web3(Web3.HTTPProvider(c.ARBITRUM_MAINNET))
eth_main = Web3(Web3.HTTPProvider(c.ETHEREUM_MAINNET))

def contract_interface(provider, address, abi):
    return provider.eth.contract(address=address, abi=abi)

#we use Pokt to access chain data
class Pokt():
    '''A class to collect Pokt functionality
    '''
    ...


class Translucent(Pokt):

    '''A class to collect required Translucent functionality
    '''
    gauss_arbi_goerli  = contract_interface(
            arbi_goerli,
            address=c.TRANSLUCENT_GAUSS_GOERLI_ARBITRUM,
            abi=c.TRANSLUCENT_FLUX_AGGREGATOR
        )

