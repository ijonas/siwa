import pandas as pd
import requests
from apis.evm import evm_api, rpcs
from web3 import Web3
from feeds.data_feed import DataFeed
import time
import os


class UnrealisedOVLSupply(DataFeed):
    NAME = 'unr_ovl_supply'
    ID = 10
    HEARTBEAT = 12
    SUBGRAPH_URL = 'https://gateway-arbitrum.network.thegraph.com/api/<api-key>/subgraphs/id/7RuVCeRzAHL5apu6SWHyUEVt3Ko2pUv2wMTiHQJaiUW9'  # noqa: E501
    MULTICALL_ADDRESS = '0x842eC2c7D803033Edf55E478F461FC547Bc54EB2'
    STATE_ADDRESS = '0xC3cB99652111e7828f38544E3e94c714D8F9a51a'

    rpc_urls = list(rpcs.get_rpc_urls(rpcs.ARBITRUM_ONE).values())
    multicall_api = evm_api.EVM_API(rpc_urls, MULTICALL_ADDRESS,
                                    'aggregate', connect=True)
    state_api = evm_api.EVM_API(rpc_urls, STATE_ADDRESS, connect=True)

    @staticmethod
    def _read_api_key(self):
        try:
            graph_api_key = os.environ['GRAPH_API_KEY']
        except KeyError:
            raise Exception("GRAPH_API_KEY not set")
        return graph_api_key

    @classmethod
    def query_subgraph(cls, first, skip):
        query = f'''
        {{
            builds(first: {first}, skip: {skip}) {{
                collateral
                id
                position {{
                    currentOi
                    fractionUnwound
                }}
                owner {{
                    id
                }}
            }}
        }}
        '''
        cls.SUBGRAPH_URL = cls.SUBGRAPH_URL.replace(
            '<api-key>',
            cls._read_api_key('GRAPH_API_KEY')
        )
        response = requests.post(cls.SUBGRAPH_URL, json={'query': query})
        data = response.json().get('data', {}).get('builds', [])
        return data

    @classmethod
    def get_value_calls(cls, data_frame):
        calls = []
        for _, row in data_frame.iterrows():
            call_data = cls.state_api.web3.eth.contract(
                address=Web3.toChecksumAddress(cls.STATE_ADDRESS),
                abi=cls.state_api.abi
            ).encodeABI(
                fn_name='value',
                args=[
                    Web3.toChecksumAddress(row['market']),
                    Web3.toChecksumAddress(row['owner.id']),
                    int(row['position_id'])
                ]
            )
            calls.append((cls.STATE_ADDRESS, call_data))
        return calls

    @staticmethod
    def chunked_multicall(calls, chunk_size=100):
        # Break the calls into chunks of specified size
        for i in range(0, len(calls), chunk_size):
            yield calls[i:i + chunk_size]

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        # Query the subgraph and paginate through results
        skip = 0
        all_data = []
        while True:
            data = cls.query_subgraph(1000, skip)
            if not data:
                break
            all_data.extend(data)
            skip += 1000

        # Process data into DataFrame
        df = pd.json_normalize(all_data)
        df[['market', 'position_id']] = df['id'].str.split('-', expand=True)
        df['position_id'] = df['position_id'].apply(lambda x: int(x, 16))
        df['collateral'] = df['collateral'].astype(float)/1e18
        df['position.fractionUnwound'] = df['position.fractionUnwound'].astype(float)/1e18  # noqa: E501
        df['position.currentOi'] = df['position.currentOi'].astype(float)/1e18
        df = df[df['position.currentOi'] > 0]  # Get live positions only
        # Adjust collateral based on position unwound
        df['collateral_rem'] =\
            df['collateral'] * (1 - df['position.fractionUnwound'])

        # Get the value calls for multicall
        value_calls = cls.get_value_calls(df)
        # value_calls = [value_calls[0] for call in value_calls]
        all_values = []
        counter = 0
        latest_block = cls.state_api.web3.eth.get_block('latest')
        latest_block = latest_block['number']
        for chunk in cls.chunked_multicall(value_calls, 750):
            # Set multicall API function name and arguments for the chunk
            cls.multicall_api.args = [chunk]

            # Execute multicall for the chunk
            response = cls.multicall_api.get_values(block=latest_block)
            counter += 1
            print(f"Processed chunk {counter}")
            time.sleep(0.2)

            # Decode the response data for the chunk
            chunk_values = [int.from_bytes(val, 'big') for val in response[1]]

            # Add the chunk's values to the all_values list
            all_values.extend(chunk_values)

        df['value'] = [val/1e18 for val in all_values]
        df['upnl'] = df['value'] - df['collateral_rem']
        upnl = df['upnl'].sum()
        return upnl

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()
