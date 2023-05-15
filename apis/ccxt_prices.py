import ccxt
import numpy as np


def fetch_average_prices(exchanges, pairs):
    prices = {pair: [] for pair in pairs}

    for exchange_id in exchanges:
        exchange = getattr(ccxt, exchange_id)()

        for pair in pairs:
            data = exchange.fetch_ticker(pair)
            latest_price = data['last']
            prices[pair].append(latest_price)

    average_prices = {pair: np.mean(prices_list) for pair, prices_list in prices.items()}

    return average_prices


exchanges = ['coinbasepro']
pairs = ['UNI/USD', 'DOGE/USD']

average_prices = fetch_average_prices(exchanges, pairs)

for pair, average_price in average_prices.items():
    print(f'Avg latest price of {pair} is {average_price} USD')
