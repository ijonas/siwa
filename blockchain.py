from dataclasses import dataclass
import constants as c
from numpy import random
from web3 import Web3



arbi_goerli = Web3(Web3.HTTPProvider(c.ARBITRUM_GOERLI_RPC))
arbi_main = Web3(Web3.HTTPProvider(c.ARBITRUM_MAINNET_RPC))
eth_main = Web3(Web3.HTTPProvider(c.ETHEREUM_MAINNET_RPC))

def contract_interface(provider, address, abi):
    return provider.eth.contract(address=address, abi=abi)

#we use Pokt to access chain data
class Pokt():
    '''A class to collect Pokt functionality
    '''
    ...


class Translucent:

    '''A class to collect Translucent functionality
    '''
    gauss_arbi_goerli  = contract_interface(
            arbi_goerli,
            address=c.TRANSLUCENT_GAUSS_ARBITRUM_GOERLI,
            abi=c.TRANSLUCENT_FLUX_AGGREGATOR
        )
    #currently unsupported
    # gauss_arbi_main  = contract_interface(
    #         arbi_main,
    #         address=c.TRANSLUCENT_GAUSS_ARBITRUM_MAINNET,
    #         abi=c.TRANSLUCENT_FLUX_AGGREGATOR
    #     )



    faceripper_arbi_goerli  = contract_interface(
            arbi_goerli,
            address=... ,
            abi=c.TRANSLUCENT_FLUX_AGGREGATOR
        )
    #currently unsupported
    # faceripper_arbi_main  = contract_interface(
    #         arbi_main,
    #         address=c.TRANSLUCENT_GAUSS_ARBITRUM_MAINNET,
    #         abi=c.TRANSLUCENT_FLUX_AGGREGATOR
    #     )