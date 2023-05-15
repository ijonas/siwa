import ccxt

def get_common_markets(exchanges):
    exchange_markets = []

    for exchange_id in exchanges:
        exchange = getattr(ccxt, exchange_id)()
        markets = exchange.load_markets()
        exchange_markets.append(set(markets.keys()))

    common_markets = set.intersection(*exchange_markets)
    
    return common_markets

exchanges = ['binance', 'coinbasepro']

common_markets = get_common_markets(exchanges)
common_markets_stable = [market for market in common_markets if market.endswith('/USD') | market.endswith('/USDT') | market.endswith('/USDC')]

for market in common_markets_stable:
    print(market)
