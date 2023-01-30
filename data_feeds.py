import logging
import pandas as pd
import constants as c
from dataclasses import dataclass



@dataclass
class DataFeed:
    name = ''
    heartbeat = 0
    active = False
    data_dir = DATA_DIR / name




    def get_data_point():
	raise NotImplementedError



