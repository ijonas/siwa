import os


# List of networks
ARBITRUM_ONE = 'arbitrum_one'


# List of providers
ALCHEMY = 'ALCHEMY'
INFURA = 'INFURA'
POKT = 'POKT'


# RPC URLs for each provider and each network
RPCS = {
    ARBITRUM_ONE: {
        ALCHEMY: 'https://arb-mainnet.g.alchemy.com/v2/',
        INFURA: 'https://arb1.infura.io/v3/',
        POKT: 'https://arbitrum-one.gateway.pokt.network/v1/lb/'
    }
}


def _read_api_key(key_name):
    # Read API keys from environment variables
    try:
        api_key = os.environ[key_name]
    except KeyError:
        print(f"{key_name} not set; skipping associated RPC URL.")
        api_key = None
    return api_key


def read_api_key(provider):
    key_name_suffix = '_API_KEY'
    api_key = _read_api_key(provider + key_name_suffix)
    return api_key


def get_rpc_urls(network):
    rpcs = RPCS[network]
    no_key = []
    for provider, url in rpcs.items():
        key = read_api_key(provider)
        if key is not None:
            rpcs[provider] = url + read_api_key(provider)
        else:
            no_key.append(provider)
    for provider in no_key:
        del rpcs[provider]
    if len(rpcs) == 0:
        raise Exception("No keys found in environment variables.")
    return rpcs
