import os


# List of networks
ARBITRUM_ONE = 'arbitrum_one'


# List of providers
ALCHEMY = 'alchemy'
INFURA = 'infura'
POKT = 'pokt'


# RPC URLs for each provider and each network
RPCS = {
    ARBITRUM_ONE: {
        ALCHEMY: 'https://arb-mainnet.g.alchemy.com/v2/',
        INFURA: 'https://arb1.infura.io/v3/',
        POKT: 'https://arbitrum-one.gateway.pokt.network/v1/lb/'
    }
}


def read_api_key(key_name):
    # Read API keys from environment variables
    try:
        api_key = os.environ[key_name]
    except KeyError:
        print(f"{key_name} not set; skipping associated RPC URL.")
    return api_key


def append_api_key(provider):
    key_name_suffix = '_api_key'
    api_key = read_api_key(provider + key_name_suffix)
    return api_key


def get_rpc_urls(network):
    rpcs = RPCS[network]
    for provider, url in rpcs.items():
        rpcs[provider] = url + append_api_key(provider)
    return rpcs
