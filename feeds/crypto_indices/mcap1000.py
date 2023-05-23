from feeds.data_feed import DataFeed
import apis.coingecko as cgecko
import apis.coinmarketcap as cmc
from collections import deque 


class MCAP1000(DataFeed):
    NAME = 'mcap1000'
    ID = 2 
    HEARTBEAT = 180
    DATAPOINT_DEQUE = deque([], maxlen=100)
    N = 10

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        '''
            Process data from multiple sources
        '''
        res = []
        for source in [cmc, cgecko]:
            market_data = source.fetch_data_by_mcap(cls.N)
            if market_data is None:
                return cls.DATAPOINT_DEQUE[-1]  # This should fail if DEQUE is empty
            mcaps = sorted(list(market_data.keys()), reverse=True)
            res.append(sum(mcaps[:cls.N]))
        # Take average of values from both sources
        result = sum(res) / len(res)
        return result

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()

# if __name__ == '__main__':
#     MCAP1000.process_source_data_into_siwa_datapoint() 