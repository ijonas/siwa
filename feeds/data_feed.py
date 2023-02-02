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
    NAME: str = ''
    FEED_ID: int = ...
    HEARTBEAT: int = ...  #in seconds

    def __init__(self, printdata=False):
        self.active: bool = False
        self.data_dir: c.Path = c.DATA_PATH / (self.NAME + c.DATA_EXT)
        self.pidfile_path: c.Path = self.data_dir / str(self.FEED_ID)
        self.pidfile_timeout: int = 5
        self.printdata = printdata
    #logging:


    def run(self, printdata=False):
        logging.info(f'Starting {self.NAME} data feed!')

        while True:
            dp = self.get_data_point()
            if self.printdata:
                print(f'Next data point for {self.NAME}: {dp}')
            self.save_data_point(dp)
            time.sleep(self.HEARTBEAT)


    def get_data_point():
        raise NotImplementedError


    def save_data_point(self, dp):
        with Lock():
            with open(self.data_dir, 'a+') as datafile:
                datafile.write(self.format_data(dp))


    @staticmethod
    def format_data(dp):
        timenow =  datetime.now(timezone.utc)
        strtime = timenow.strftime(c.DATEFORMAT)
        return f'{strtime}, {dp}, \n'
