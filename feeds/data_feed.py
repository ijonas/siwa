import time
import logging
import pandas as pd
import typing as tp
import constants as c
from dataclasses import dataclass



@dataclass
class DataFeed:
    name: str = ''
    heartbeat: int = ...  #in seconds
    active: bool = False
    data_dir: c.Path = c.DATA_PATH / name
    feed_id: int = ...
    pidfile_path: c.Path = data_dir / str(feed_id)
    pidfile_timeout: int = 5


    def run(self):
        print(f'Starting {self.name} data feed!')

        while True:
            print(f'Fetching next data point for {self.name}')

            print(self.get_data_point(), '\n')
            time.sleep(self.heartbeat)

    def get_data_point():
        raise NotImplementedError



