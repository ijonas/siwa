import time
import logging
import pandas as pd
import typing as tp
import constants as c
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
    name: str = ''
    heartbeat: int = ...  #in seconds
    active: bool = False
    data_dir: c.Path = c.DATA_PATH / name
    feed_id: int = ...
    pidfile_path: c.Path = data_dir / str(feed_id)
    pidfile_timeout: int = 5
    #logging:


    def run(self):
        logging.info(f'Starting {self.name} data feed!')

        while True:
            dp = self.get_data_point()
            # self.save_data_point(dp)

            logging.warn(f'Next data point for {self.name}: {dp}')
            time.sleep(self.heartbeat)

    def get_data_point():
        raise NotImplementedError



