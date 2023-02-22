from feeds.data_feed import DataFeed
from dataclasses import dataclass
import constants as c
from numpy import random


class Test(DataFeed):
    NAME = 'test'
    ID = 0
    HEARTBEAT = 1
    #Feed-specific class-level attrs

    @classmethod
    def create_new_data_point(cls):
        return random.rand()
