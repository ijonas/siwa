import ccxt
import numpy as np


def fetch_average_prices(exchanges, pairs):
    prices = {pair: [] for pair in pairs}

    for exchange_id in exchanges:
        exchange = getattr(ccxt, exchange_id)()

        for pair in pairs:
            try:
                data = exchange.fetch_ticker(pair)
            except Exception as e:
                print(f'Error fetching {pair} on {exchange_id}')
                print(e)
                continue
                # TODO: Avoid instances of this error and log when it happens
            latest_price = data['last']
            print(f'Latest price of {pair} on {exchange_id} is {latest_price} USD')
            prices[pair].append(latest_price)

    average_prices = {pair: np.mean(prices_list) for pair, prices_list in prices.items()}

    return average_prices


exchanges = ['coinbasepro', 'binance', 'kraken']
pairs = ['BTC/USD', 'ETH/USD', 'USDT/USD']

average_prices = fetch_average_prices(exchanges, pairs)

for pair, average_price in average_prices.items():
    print(f'Avg latest price of {pair} is {average_price} USD')
