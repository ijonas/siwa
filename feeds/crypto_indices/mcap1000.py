from feeds.data_feed import DataFeed
from collections import deque

import apis.coingecko as cgecko
import apis.coinmarketcap as cmc
from apis import (coingecko, coinmarketcap, coinpaprika)


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
        for source in [
            coinpaprika,
            coinmarketcap,
            coingecko
        ]:
            market_data = source.fetch_data_by_mcap(cls.N)
            if market_data is None:
                continue
            mcaps = sorted(list(market_data.keys()), reverse=True)
            res.append(sum(mcaps[:cls.N]))
        if sum(res) == 0:
            return cls.DATAPOINT_DEQUE[-1]  # Should fail if DEQUE is empty
        else:
            # Take average of values from all sources
            return sum(res) / len(res)

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()

# if __name__ == '__main__':
#     MCAP1000.process_source_data_into_siwa_datapoint() 