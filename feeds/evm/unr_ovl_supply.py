import pandas as pd
import requests
from collections import deque
from web3 import Web3
import time
import os
from apis.evm import evm_api, rpcs
from apis.thegraph.thegraph_api import GraphQueryWithPagination
from feeds.data_feed import DataFeed


class UnrealisedOVLSupply(DataFeed):
    NAME = 'unr_ovl_supply'
    ID = 10
    HEARTBEAT = 30
    DATAPOINT_DEQUE = deque([], maxlen=100)
    SUBGRAPH_URL = 'https://gateway-arbitrum.network.thegraph.com/api/<api-key>/subgraphs/id/7RuVCeRzAHL5apu6SWHyUEVt3Ko2pUv2wMTiHQJaiUW9'  # noqa: E501
    MULTICALL_ADDRESS = '0x842eC2c7D803033Edf55E478F461FC547Bc54EB2'
    STATE_ADDRESS = '0xC3cB99652111e7828f38544E3e94c714D8F9a51a'
    OVL_ADDRESS = '0x4305C4Bc521B052F17d389c2Fe9d37caBeB70d54'

    rpc_urls = list(rpcs.get_rpc_urls(rpcs.ARBITRUM_ONE).values())
    multicall_api = evm_api.EVM_API(rpc_urls, MULTICALL_ADDRESS,
                                    'aggregate', connect=True)
    state_api = evm_api.EVM_API(rpc_urls, STATE_ADDRESS, connect=True)
    ovl_api = evm_api.EVM_API(rpc_urls, OVL_ADDRESS,
                              'totalSupply', connect=True)
    graph_query = GraphQueryWithPagination(
        subgraph_id='7RuVCeRzAHL5apu6SWHyUEVt3Ko2pUv2wMTiHQJaiUW9',
        data_path=['builds']
    )

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

    @staticmethod
    def process_data_into_dataframe(data):
        '''
        Process data into a DataFrame for easier manipulation
        '''
        df = pd.json_normalize(data)
        df[['market', 'position_id']] = df['id'].str.split('-', expand=True)
        df['position_id'] = df['position_id'].apply(lambda x: int(x, 16))
        df['collateral'] = df['collateral'].astype(float)/1e18
        df['position.fractionUnwound'] =\
            df['position.fractionUnwound'].astype(float)/1e18
        df['position.currentOi'] = df['position.currentOi'].astype(float)/1e18
        df = df[df['position.currentOi'] > 0]  # Get live positions only
        # Adjust collateral based on position unwound
        df['collateral_rem'] =\
            df['collateral'] * (1 - df['position.fractionUnwound'])
        return df

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        # Generate the GraphQL query
        query = """
        query GetBuilds($startTime: Int!, $endTime: Int!, $first: Int!) {
            builds(where: { timestamp_gt: $startTime, timestamp_lte: $endTime }, first: $first, orderBy: timestamp, orderDirection: asc) {
                collateral
                timestamp
                id
                position {
                    currentOi
                    fractionUnwound
                }
                owner {
                    id
                }
            }
        }
        """
        start_time, end_time = 1637038771, 1700110816

        # Paginate through the data based on timestamps
        variables = {
            'startTime': start_time,
            'endTime': end_time,
            'first': 1000  # Adjust the number accordingly
        }

        all_data = cls.graph_query.execute_paginated_query(
            query,
            variables=variables,
            page_size=1000  # The Graph's max results limit per query
        )

        # Process data into DataFrame
        df = cls.process_data_into_dataframe(all_data)

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
        ovl_supply = cls.ovl_api.get_values()
        unr_ovl_sup = (ovl_supply/1e18) + upnl
        return unr_ovl_sup

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()
