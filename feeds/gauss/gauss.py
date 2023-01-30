from data_feed import DataFreed
from numpy import random

class Gaussian(DataFeed):
    def __init__(self):
        self.pct = .01
        self.vol = 1
        self.heartbeat = 10


    def get_latest_data_point():
        '''
        How to get latest data point from blockchain?
        '''
        ...


    def get_next_data_point(x)
        std = max(self.vol * x * self.pct, .001)
        delta = random.normal(0, std)
        return self.vol * delta


    def get_data_point(x):
        '''
        NOTE:
            This method requires the last data point of the actual feed deployed on the blockchain
            This is because the variance of the distribution (determining the next data point) is a function of the last data point
        '''
        x = self.get_latest_data_point()
        return get_next_data_point(x)
