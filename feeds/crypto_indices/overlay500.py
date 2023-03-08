from feeds.data_feed import DataFeed
from collections import deque 
from dataclasses import dataclass
import constants as c
from numpy import random


class Overlay500(DataFeed):
    NAME = 'overlay500'
    ID = 2 
    HEARTBEAT = 60
    DATAPOINT_DEQUE = deque([], maxlen=100)

    @classmethod
    def create_new_data_point(cls):
        return random.rand()
