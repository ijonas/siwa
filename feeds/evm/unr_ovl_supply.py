import requests
from apis.evm import evm_api, rpcs
from web3 import Web3

# Constants
SUBGRAPH_URL = 'https://api.studio.thegraph.com/query/1234/your-subgraph/v0.0.1'  # NOQA E501
MULTICALL_ADDRESS = '0x842eC2c7D803033Edf55E478F461FC547Bc54EB2'
OVERLAY_V1_ADDRESS = '0xc3cb99652111e7828f38544e3e94c714d8f9a51a'

# Initialize EVM_API instances
rpc_urls = list(rpcs.get_rpc_urls(rpcs.ARBITRUM_ONE).values())
multicall_api = evm_api.EVM_API(rpc_urls, MULTICALL_ADDRESS, connect=True)
overlay_api = evm_api.EVM_API(rpc_urls, OVERLAY_V1_ADDRESS, connect=True)


# Pagination query function
def query_subgraph(skip):
    query = '''
    {
        builds(first: 100, skip: %s) {
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
    ''' % skip
    response = requests.post(SUBGRAPH_URL, json={'query': query})
    data = response.json().get('data', {}).get('builds', [])
    return data


# Function to encode calls for multicall
def get_value_calls(data_frame):
    calls = []
    for index, row in data_frame.iterrows():
        call_data = overlay_api.web3.eth.contract(
            address=Web3.toChecksumAddress(OVERLAY_V1_ADDRESS),
            abi=overlay_api.abi
        ).encodeABI(
            fn_name='value',
            args=[
                Web3.toChecksumAddress(row['market']),
                Web3.toChecksumAddress(row['owner.id']),
                int(row['position_id'])
            ]
        )
        calls.append((OVERLAY_V1_ADDRESS, call_data))
    return calls
