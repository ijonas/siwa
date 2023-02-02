import time
import logging
import pandas as pd
import typing as tp
import constants as c
from threading import Lock
from datetime import datetime, timezone
from dataclasses import dataclass

# logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s:%(thread)d - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter
logger = logging.getLogger('SQLLogger')
logger.setLevel(logging.INFO)
# logger.addHandler(ch)
logging.basicConfig(
        filename=c.LOGGING_PATH,
        filemode='a+',
        format=('%(asctime)s:%(thread)d - %(name)s - %(levelname)s - %(message)s')
        )


@dataclass
class DataFeed:
    ''' The base-level implementation for all data feeds, which should inherit from DataFeed and implement the get_data_point method as required.
    '''
    #NOTE: all feeds must define these class-level attributes
    NAME: str = ''
    FEED_ID: int = ...
    HEARTBEAT: int = ...  #in seconds


    @classmethod
    def get_data_dir(cls):
        return c.DATA_PATH / (cls.NAME + c.DATA_EXT)

    @classmethod
    def run(cls, printdata=False):
        logging.info(f'Starting {cls.NAME} data feed!')

        while True:
            dp = cls.get_data_point(cls)
            if printdata:
                print(f'Next data point for {cls.NAME}: {dp}')
            cls.save_data_point(dp)
            time.sleep(cls.HEARTBEAT)

    @classmethod
    def get_data_point(cls):
        raise NotImplementedError


    @classmethod
    def save_data_point(cls, dp):
        with Lock():
            with open(cls.get_data_dir(), 'a+') as datafile:
                datafile.write(cls.format_data(dp))


    @staticmethod
    def format_data(dp):
        timenow =  datetime.now(timezone.utc)
        strtime = timenow.strftime(c.DATEFORMAT)
        return f'{strtime}, {dp}, \n'
