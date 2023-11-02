from feeds.data_feed import DataFeed
from collections import deque

from apis.evm import evm_api, rpcs


class EthBurnRate(DataFeed):
    NAME = 'eth_burn_rate'
    ID = 9
    HEARTBEAT = 300
    DATAPOINT_DEQUE = deque([], maxlen=100)

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        '''
        Process source data into siwa datapoint
        '''
        res = []
        eth_rpcs = rpcs.get_rpc_urls('ethereum')
        eth_rpcs = eth_rpcs.values()
        eth = evm_api.EVM_API(eth_rpcs, connect=True)
        latest_blk = eth.web3.eth.get_block('latest')
        burn_rate = latest_blk.baseFeePerGas * latest_blk.gasUsed/1e18
        if burn_rate == 0:
            return cls.DATAPOINT_DEQUE[-1]  # Should fail if DEQUE is empty
        else:
            res.append(burn_rate)
            return burn_rate

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()
