from feeds.data_feed import DataFeed
import apis.coingecko as cgecko
from collections import deque 
import constants as c


class DogCoins(DataFeed):
    NAME = 'dogcoins'
    ID =  7
    HEARTBEAT = 180
    DATAPOINT_DEQUE = deque([], maxlen=100)
    CGECKO_IDS = [c.DOGE, c.BABYDOGE, c.DOGELON, c.SHIBA, c.SHIBASWAP] 

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        '''
        '''
        market_data = cgecko.fetch_data_from_web(cls.CGECKO_IDS) 
        if market_data is None:
            return cls.DATAPOINT_DEQUE[-1]  #This should fail if DEQUE is empty
        mcaps = sorted(list(market_data.keys()), reverse=True)
        res =  sum(mcaps[:cls.N])
        return res

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()
