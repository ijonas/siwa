from feeds.data_feed import DataFeed
from collections import deque

from apis.coinmarketcap import CoinMarketCapAPI as coinmarketcap
from apis.coingecko import CoinGeckoAPI as coingecko
from apis.cryptocompare import CryptoCompareAPI as cryptocompare


class BTCDom(DataFeed):
    NAME = 'btc_dominance'
    ID = 11
    HEARTBEAT = 180
    DATAPOINT_DEQUE = deque([], maxlen=100)
    COINGECKO = 'coingecko'
    COINMARKETCAP = 'coinmarketcap'
    CRYPTOCOMPARE = 'cryptocompare'
    SOURCES = [COINGECKO, COINMARKETCAP, CRYPTOCOMPARE]
    TOKEN_MAP = {
        'bitcoin': {
            COINGECKO: 'bitcoin',
            COINMARKETCAP: 1,
            CRYPTOCOMPARE: 'BTC'
        }
    }

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        '''
        Process source data into siwa datapoint
        '''
        res = []
        sources = [globals().get(obj) for obj in cls.SOURCES]
        for i, source in enumerate(sources):
            ids = []
            for item in cls.TOKEN_MAP:
                ids.append(cls.TOKEN_MAP[item][cls.SOURCES[i]])
            market_data = source().fetch_mcap_by_list(ids)
            if market_data is None:
                continue
            mcaps = sorted(list(market_data.keys()), reverse=True)
            breakpoint()
            res.append(sum(mcaps))
        if sum(res) == 0:
            return cls.DATAPOINT_DEQUE[-1]  # Should fail if DEQUE is empty
        else:
            # Take average of values from all sources
            return sum(res) / len(res)

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()
