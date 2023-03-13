from feeds.data_feed import DataFeed
import apis.coingecko as cgecko
from collections import deque 
import constants as c


class StableCoin(DataFeed):
    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        '''
        '''
        market_data = cgecko.fetch_data_from_web([cls.CGECKO_ID])
        if market_data is None:
            return cls.DATAPOINT_DEQUE[-1]
        px = market_data[cls.CGECKO_ID][c.PRICE]
        return px 

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()



class USDC(StableCoin):
    NAME = 'usdc'
    ID = 3 
    HEARTBEAT = 120 
    DATAPOINT_DEQUE = deque([], maxlen=100)
    CGECKO_ID = c.USDC


class BUSD(StableCoin):
    NAME = 'busd'
    ID = 4 
    HEARTBEAT = 120 
    DATAPOINT_DEQUE = deque([], maxlen=100)
    CGECKO_ID = c.BUSD

class Tether(StableCoin):
    NAME = 'tether'
    ID = 5 
    HEARTBEAT = 120 
    DATAPOINT_DEQUE = deque([], maxlen=100)
    CGECKO_ID = c.TETHER


class Dai(StableCoin):
    NAME = 'dai'
    ID = 6 
    HEARTBEAT = 120 
    DATAPOINT_DEQUE = deque([], maxlen=100)
    CGECKO_ID = c.DAI