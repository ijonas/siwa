#stdlib
import os
import time
import logging
import typing as tp
from threading import Lock
from collections import deque 
from datetime import datetime, timezone
from dataclasses import dataclass

#third party
import pandas as pd

#our stuff
import constants as c
import siwa_logging

#'%(asctime)s:%(thread)d - %(name)s - %(levelname)s - %(message)s') 
logger = logging.getLogger('SQLLogger')
logger.setLevel(logging.INFO)
logger.addHandler(siwa_logging.SQLite_Handler())
logger.propagate = False # TODO determine if undesirable

@dataclass
class DataFeed:
    ''' The base-level implementation for all data feeds, which should inherit from DataFeed and implement the get_data_point method as required.
    '''

    #NOTE: all feeds must define these class-level attributes
    NAME: str
    ID: int
    HEARTBEAT: int              #in seconds
    START_TIME: float #unix timestamp
    ACTIVE: bool = False
    COUNT: int = 0              #number of data points served since starting

    DATA_KEYS = (c.FEED_NAME, c.TIME_STAMP, c.DATA_POINT)
    DATAPOINT_DEQUE = deque([], maxlen=100)

    @classmethod
    def get_data_dir(cls):
        return c.DATA_PATH / (cls.NAME + c.DATA_EXT)

    @classmethod
    def run(cls):
        while cls.ACTIVE:
            dp = cls.create_new_data_point()
            logger.info(f'\nNext data point for {cls.NAME}: {dp}\n')
            cls.DATAPOINT_DEQUE.append(dp)
            cls.COUNT += 1
            time.sleep(cls.HEARTBEAT)

    @classmethod
    def create_new_data_point(cls):
        ''' ? '''
        raise NotImplementedError

    @classmethod
    def get_most_recently_stored_data_point(cls):
        ''' pass '''
        if len(cls.DATAPOINT_DEQUE):
            return cls.DATAPOINT_DEQUE[-1]
        else:
            return None

    @staticmethod
    def format_data(dp):
        timenow =  datetime.now(timezone.utc)
        strtime = timenow.strftime(c.DATEFORMAT)
        return f'{c.LINE_START}{strtime},{dp},\n'
