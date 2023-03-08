from feeds.data_feed import DataFeed
import apis.coingecko as cgecko
from collections import deque 


class MCAP1000(DataFeed):
    NAME = 'mcap_1000'
    ID = 2 
    HEARTBEAT = 180
    DATAPOINT_DEQUE = deque([], maxlen=100)
    N = 1000

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        '''
        '''
        market_data = cgecko.fetch_data_by_mcap(cls.N) 
        mcaps = sorted(list(market_data.keys()), reverse=True)
        res =  sum(mcaps[:cls.N])/cls.N
        return res

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()

# if __name__ == '__main__':
#     MCAP1000.process_source_data_into_siwa_datapoint() 