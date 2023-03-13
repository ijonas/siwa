from feeds.data_feed import DataFeed
import apis.coingecko as cgecko
from collections import deque 


class USDC(DataFeed):
    NAME = 'usdc'
    ID = 3 
    HEARTBEAT = 120 
    DATAPOINT_DEQUE = deque([], maxlen=100)
    CGECKO_ID = 'usd-coin'

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        '''
        '''
        market_data = cgecko.fetch_data_from_web(cls.CGECKO_ID)) 
        if market_data is None:
            return cls.DATAPOINT_DEQUE[-1]
        breakpoint()
        return res

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()



class BUSD(DataFeed):
    NAME = 'busd'
    ID = 4 
    HEARTBEAT = 120 
    DATAPOINT_DEQUE = deque([], maxlen=100)
    CGECKO_ID = 'binance-usd'

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        '''
        '''
        market_data = cgecko.fetch_data_from_web(cls.CGECKO_ID)) 
        if market_data is None:
            return cls.DATAPOINT_DEQUE[-1]
        return res

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()