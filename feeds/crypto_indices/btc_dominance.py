from feeds.data_feed import DataFeed
from collections import deque

from apis.coinmarketcap import CoinMarketCapAPI as coinmarketcap
from apis.coingecko import CoinGeckoAPI as coingecko
from apis.cryptocompare import CryptoCompareAPI as cryptocompare
from apis.evm import evm_api, rpcs


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
    CHAINLINK_FEED_ADDRESS = '0xec8761a0a73c34329ca5b1d3dc7ed07f30e836e2'
    RPC_URLS = list(rpcs.get_rpc_urls(rpcs.ETHEREUM).values())
    DECIMALS = evm_api.EVM_API(RPC_URLS, CHAINLINK_FEED_ADDRESS,
                               'decimals', connect=True).get_values()

    @classmethod
    def get_bitcoin_marketcap(cls):
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
            res.append(sum(mcaps))
        # Take average of values from all sources
        return sum(res) / len(res)

    @classmethod
    def get_total_crypto_marketcap(cls):
        chainlink_api = evm_api.EVM_API(cls.RPC_URLS,
                                        cls.CHAINLINK_FEED_ADDRESS,
                                        'latestRoundData', connect=True)
        latest_round_data = chainlink_api.get_values()
        total_mcap = latest_round_data[1]/10**cls.DECIMALS
        return total_mcap

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        btc = cls.get_bitcoin_marketcap()
        if btc == 0:
            return cls.DATAPOINT_DEQUE[-1]  # Should fail if DEQUE is empty
        else:
            total_mcap = cls.get_total_crypto_marketcap()
            return btc/total_mcap

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()
