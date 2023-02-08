from feeds.data_feed import DataFeed
from dataclasses import dataclass
import constants as c
from numpy import random


class Gauss(DataFeed):

    NAME = 'gauss'
    ID = 1
    HEARTBEAT = 10
    #Feed-specific class-level attrs
    PERCENT = .01
    VOLATILITY = 1


    @staticmethod
    def get_latest_data_point():
        '''
        How to get latest data point from blockchain?
        '''
        return 100


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
