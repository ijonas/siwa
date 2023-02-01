from feeds.data_feed import DataFeed
from dataclasses import dataclass
import constants as c
from numpy import random

@dataclass
class Gauss(DataFeed):
    pct: float = .01
    vol: float = 1
    heartbeat: float = 10
    name: str = 'gauss'
    active: bool = False
    feed_id: int = 0
    # pidfile_path: c.Path = data_dir + feed_id
    # pidfile_timeout: int = 5


    @staticmethod
    def get_latest_data_point():
        '''
        How to get latest data point from blockchain?
        '''
        return 100

    @classmethod
    def get_next_data_point(cls, x):
        std = max(cls.vol * x * cls.pct, .001)
        delta = random.normal(0, std)
        return x + cls.vol * delta

    @classmethod
    def get_data_point(cls):
        '''
        NOTE:
            This method requires the last data point of the actual feed deployed on the blockchain
            This is because the variance of the distribution (determining the next data point) is a function of the last data point
        '''
        x = cls.get_latest_data_point()
        return cls.get_next_data_point(x)
