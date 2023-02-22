#standard library
from collections import deque 
from dataclasses import dataclass

#3rd party
from web3 import Web3
from numpy import random

#our stuff
import constants as c
from feeds.data_feed import DataFeed
from blockchain import Translucent

class Gauss(DataFeed):
    CHAIN = c.ARBITRUM_GOERLI
    NAME = 'gauss'
    ID = 1
    HEARTBEAT = 1
    DATAPOINT_DEQUE = deque([], maxlen=100)
    #Feed-specific class-level attrs
    PERCENT = .01
    VOLATILITY = 1

    @classmethod
    def get_latest_source_data(cls):
        ''' fetch data from datasource; in this case, the blockchain'''
        #TODO TBD: return None if datum already seen?
        if cls.CHAIN == c.ARBITRUM_GOERLI:
            gauss = Translucent.gauss_arbi_goerli
        elif cls.CHAIN == c.ARBITRUM_MAINNET:
            return Translucent.gauss_arbi_main

        return gauss.functions.latestAnswer().call()

    @classmethod
    def process_source_data_into_siwa_datapoint(cls, source_data):
        ''' We have a dynamic standard deviation, based on the last data point, so we can get a new data point
            that is within a certain percentage of the last data point. Without this, if the previous data point
            is large, the delta (between previous and new) will be very small, and vice versa.
        '''
        std = max(cls.VOLATILITY * source_data * cls.PERCENT, .001)
        delta = random.normal(0, std)
        return source_data + cls.VOLATILITY * delta

    @classmethod
    def create_new_data_point(cls):
        ''' fetches data from datasource,
            applies siwa algorithms to create new siwa datapoint,
            returns said new siwa datapoint (or None if datasource stale?? TBD)
        NOTE:
            This method requires the last data point of the actual feed deployed on the blockchain
            This is because the variance of the distribution (determining the next data point) is a function of the last data point
        '''
        #NOTE TODO / BUG POTENTIAL / should we check and ensure latest datasource data
        #is new and we haven't seen it before? Or is that irrelevant?
        source_data = cls.get_latest_source_data()
        # print(f'got source data and it is {source_data}') #manually checking functionality
        return cls.process_source_data_into_siwa_datapoint(source_data)
