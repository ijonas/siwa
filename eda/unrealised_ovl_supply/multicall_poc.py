import json
from web3 import Web3

# Your Ethereum node URL
NODE_URL = 'https://arb-mainnet.g.alchemy.com/v2/<PASTE_KEY>'

# Multicall contract address and ABI (replace with the actual ABI from Arbiscan)
MULTICALL_ADDRESS = '0x842eC2c7D803033Edf55E478F461FC547Bc54EB2'

# Token contract details
TOKEN_ADDRESS = '0x4305C4Bc521B052F17d389c2Fe9d37caBeB70d54'

# Addresses to query
addresses = [
    '0xaC5FCBeD890EeeaAbe00F1Aa5A79e6AB252cC278',
    '0x27014500207436F0395ab6222c7Aa66ABBb816d2'
]

def get_token_abi():
    with open('token_abi.json', 'r') as f:
        abi = json.load(f)
    return abi

def get_multicall_abi():
    with open('multicall_abi.json', 'r') as f:
        abi = json.load(f)
    return abi

MULTICALL_ABI = get_multicall_abi()
TOKEN_ABI = get_token_abi()

def get_token_balance_calls(token_contract, addresses):
    calls = []
    for address in addresses:
        call_data = token_contract.encodeABI(fn_name='balanceOf', args=[address])
        calls.append((TOKEN_ADDRESS, call_data))
    return calls

def get_latest_block_number(w3):
    return w3.eth.getBlock('latest')['number']

def query_balances(w3, multicall_contract, calls, block_number='latest'):
    if block_number == 'latest':
        block_number = get_latest_block_number(w3)
    # If a block number is provided, use it in the call to query historical balances
    response = multicall_contract.functions.aggregate(calls).call(block_identifier=block_number)
    return response[1]  # The return data is in the second element

def main():
    # Create a Web3 connection
    w3 = Web3(Web3.HTTPProvider(NODE_URL))

    # Ensure the node is connected
    if not w3.isConnected():
        print("Unable to connect to the Ethereum node.")
        return

    # Create the Multicall and token contract instances
    multicall_contract = w3.eth.contract(address=MULTICALL_ADDRESS, abi=MULTICALL_ABI)
    token_contract = w3.eth.contract(address=TOKEN_ADDRESS, abi=TOKEN_ABI)

    # Prepare the Multicall calls for token balances
    balance_calls = get_token_balance_calls(token_contract, addresses)

    # Query the balances using Multicall
    block_number = 116855451
    balance_data = query_balances(w3, multicall_contract, balance_calls, block_number)

    # Decode the balance data
    balances = [int.from_bytes(balance, 'big') for balance in balance_data]

    # Output the results
    for address, balance in zip(addresses, balances):
        print(f'Address: {address}, Balance: {balance}')

# Run the main function
main()
