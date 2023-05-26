from apis import utils


class CryptoAPI:
    def __init__(self, url, source):
        self.url = url
        self.source = source

    def fetch_data_by_mcap(self, N):
        data = self.get_data(N)
        market_data = self.extract_market_cap(data)

        # Store market data in the database
        utils.create_market_cap_database()
        utils.store_market_cap_data(
            market_data=market_data, source=self.source
        )
        return market_data

    def get_data(self, N):
        raise NotImplementedError

    def extract_market_cap(self, data):
        raise NotImplementedError
