from feeds.data_feed import DataFeed
from dataclasses import dataclass
import constants as c
from numpy import random

class Gauss(DataFeed):
    NAME = 'Gauss'
    FEED_ID = 0
    HEARTBEAT = .10

    def __init__(self, pct, vol, printdata=False):
        self.pct = pct
        self.vol = vol
        super().__init__(printdata=printdata)


    @staticmethod
    def get_latest_data_point():
        '''
        How to get latest data point from blockchain?
        '''
        return 100

    def get_next_data_point(self, x):
        std = max(self.vol * x * self.pct, .001)
        delta = random.normal(0, std)
        return x + self.vol * delta

    def get_data_point(self):
        '''
        NOTE:
            This method requires the last data point of the actual feed deployed on the blockchain
            This is because the variance of the distribution (determining the next data point) is a function of the last data point
        '''
        x = self.get_latest_data_point()
        return self.get_next_data_point(x)
