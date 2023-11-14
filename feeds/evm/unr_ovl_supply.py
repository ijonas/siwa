import pandas as pd
import requests
from apis.evm import evm_api, rpcs
from web3 import Web3
from feeds.data_feed import DataFeed
import time
from collections import deque

# Constants
SUBGRAPH_URL = 'https://api.studio.thegraph.com/query/46086/overlay-v2-subgraph-arbitrum/version/latest'  # NOQA E501
MULTICALL_ADDRESS = '0x842eC2c7D803033Edf55E478F461FC547Bc54EB2'
STATE_ADDRESS = '0xC3cB99652111e7828f38544E3e94c714D8F9a51a'

# Initialize EVM_API instances
rpc_urls = list(rpcs.get_rpc_urls(rpcs.ARBITRUM_ONE).values())
multicall_api = evm_api.EVM_API(rpc_urls, MULTICALL_ADDRESS,
                                'aggregate', connect=True)
overlay_api = evm_api.EVM_API(rpc_urls, STATE_ADDRESS, connect=True)


# Pagination query function
def query_subgraph(first, skip):
    query = '''
    {
        builds(first: %s, skip: %s) {
            collateral
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
    ''' % (first, skip)
    response = requests.post(SUBGRAPH_URL, json={'query': query})
    data = response.json().get('data', {}).get('builds', [])
    return data


# Function to encode calls for multicall
def get_value_calls(data_frame):
    calls = []
    for _, row in data_frame.iterrows():
        call_data = overlay_api.web3.eth.contract(
            address=Web3.toChecksumAddress(STATE_ADDRESS),
            abi=overlay_api.abi
        ).encodeABI(
            fn_name='value',
            args=[
                Web3.toChecksumAddress(row['market']),
                Web3.toChecksumAddress(row['owner.id']),
                int(row['position_id'])
            ]
        )
        calls.append((STATE_ADDRESS, call_data))
    return calls


def chunked_multicall(calls, chunk_size=100):
    # Break the calls into chunks of specified size
    for i in range(0, len(calls), chunk_size):
        yield calls[i:i + chunk_size]


class UnrealisedOVLSupply(DataFeed):
    NAME = 'unr_ovl_supply'
    ID = 10
    HEARTBEAT = 12

    @classmethod
    def process_source_data_into_siwa_datapoint(cls):
        # Query the subgraph and paginate through results
        skip = 0
        all_data = []
        while True:
            data = query_subgraph(1000, skip)
            if not data:
                break
            all_data.extend(data)
            skip += 1000

        # Process data into DataFrame
        df = pd.json_normalize(all_data)
        df[['market', 'position_id']] = df['id'].str.split('-', expand=True)
        df['position_id'] = df['position_id'].apply(lambda x: int(x, 16))

        # Get the value calls for multicall
        value_calls = get_value_calls(df)
        value_calls = [value_calls[0] for call in value_calls]
        all_values = []
        counter = 0
        latest_block = overlay_api.web3.eth.get_block('latest')
        latest_block = latest_block['number']
        for chunk in chunked_multicall(value_calls, 755):
            # Set multicall API function name and arguments for the chunk
            multicall_api.args = [chunk]

            # Execute multicall for the chunk
            # if counter == 6:
            #     breakpoint()
            response = multicall_api.get_values(block=latest_block)
            counter += 1
            print(f"Processing chunk {counter}")
            print("Sleeping for 0.2 seconds...")
            time.sleep(1)

            # Decode the response data for the chunk
            chunk_values = [int.from_bytes(val, 'big') for val in response[1]]

            # Add the chunk's values to the all_values list
            all_values.extend(chunk_values)

        for value in all_values:
            print(value)

    @classmethod
    def create_new_data_point(cls):
        return cls.process_source_data_into_siwa_datapoint()
