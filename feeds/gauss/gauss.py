from feeds.data_feed import DataFeed
from dataclasses import dataclass
import constants as c
from numpy import random
from web3 import Web3

#we use Pokt to access chain data
POCKET_URL = "https://<PREFIX>.gateway.pokt.network/v1/lb/<PORTAL-ID>"
provider = Web3(Web3.HTTPProvider(POCKET_URL))
print(provider.blockNumber)

class Gauss(DataFeed):

    NAME = 'gauss'
    ID = 1
    HEARTBEAT = 1
    #Feed-specific class-level attrs
    PERCENT = .01
    VOLATILITY = 1


    @classmethod
    def get_latest_data_point(cls):
        # TODO: Best would be to get latest data point from blockchain, because when multiple siwa nodes are operating this will NOT work.
        return 100
        # stored = cls.get_most_recently_stored_data_point()
        # return stored if stored else 100


    @classmethod
    def get_next_data_point(cls, x):
        std = max(cls.VOLATILITY * x * cls.PERCENT, .001)
        delta = random.normal(0, std)
        return x + cls.VOLATILITY * delta


    def get_data_point(cls):
        '''
        NOTE:
            This method requires the last data point of the actual feed deployed on the blockchain
            This is because the variance of the distribution (determining the next data point) is a function of the last data point
        '''
        x = cls.get_latest_data_point()
        return cls.get_next_data_point(x)
