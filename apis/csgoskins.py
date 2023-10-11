import pandas as pd
import requests
from utils import get_api_key


class CSGOSkins:
    """
    A class to interact with the CSGOSkins API to fetch and process skin
    prices.

    Attributes:
    ----------
    prices_endpoint : str
        The API endpoint for fetching current prices of CSGO skins.
    base_url : str
        The base URL for the CSGOSkins API.
    api_key : str
        The API key to authenticate with the CSGOSkins API.
    """
    API_PREFIX = 'CSGO'
    PRICES_ENDPOINT = 'api/v1/prices'
    PRICE_HISTORIES_ENDPOINT = 'api/v1/price-histories'
    PRICE_HISTORIES_RPM = 20
    DEFAULT_BASE_URL = 'https://csgoskins.gg/'
    DEFAULT_RANGE = 'current'
    DEFAULT_AGG = 'max'
    AUTH_TYPE = 'Bearer'
    CONTENT_TYPE = 'application/json'
    RANGE_KEY = "range"
    AGGREGATOR_KEY = "aggregator"
    DATA_KEY = 'data'
    PRICES_KEY = 'prices'
    PRICE_KEY = 'price'
    QUANTITY_KEY = 'quantity'
    MARKET_HASH_NAME_KEY = 'market_hash_name'
    AUTHORIZATION_KEY = 'Authorization'
    CONTENT_TYPE_KEY = 'Content-Type'

    def __init__(self, base_url=DEFAULT_BASE_URL):
        """
        Initializes the CSGOSkins class with the base URL and API key.

        Parameters:
        ----------
        base_url : str, optional
            The base URL for the CSGOSkins API.
        api_key : str
            The API key to authenticate with the CSGOSkins API.
        """
        self.base_url = base_url
        self.api_key = get_api_key(self.API_PREFIX)
        self.headers = {
            self.AUTHORIZATION_KEY: f"{self.AUTH_TYPE} {self.api_key}",
            self.CONTENT_TYPE_KEY: self.CONTENT_TYPE
        }

    def get_prices(self, range=DEFAULT_RANGE, agg=DEFAULT_AGG):
        """
        Fetches the current prices of CSGO skins from the API.

        Parameters:
        ----------
        range : str, optional
            The range of prices to fetch. Default is 'current'.
        agg : str, optional
            The aggregation method to use. Default is 'max'. As per API docs,
            this is ignored if `range` is set to "current".

        Returns:
        -------
        dict
            A dictionary containing the fetched data from the API.
        """
        url = self.base_url + self.PRICES_ENDPOINT
        payload = {
            self.RANGE_KEY: range,
            self.AGGREGATOR_KEY: agg
        }
        response = requests.request('GET', url,
                                    headers=self.headers, json=payload)
        data = response.json()
        return data

    def get_prices_df(self, range=DEFAULT_RANGE, agg=DEFAULT_AGG):
        """
        Fetches the prices of CSGO skins and returns them as a pandas
        DataFrame.

        Parameters:
        ----------
        range : str, optional
            The range of prices to fetch. Default is 'current'. As per API
            docs, this is ignored if `range` is set to "current".
        agg : str, optional
            The aggregation method to use. Default is 'max'.

        Returns:
        -------
        pd.DataFrame
            A DataFrame containing the fetched data from the API.
        """
        data = self.get_prices()
        df = pd.json_normalize(
            data[self.DATA_KEY],
            record_path=self.PRICES_KEY,
            meta=self.MARKET_HASH_NAME_KEY
        )
        df.price = df.price/100
        return df

    def agg_data(self, df):
        """
        Aggregates the data of a given DataFrame by 'market_hash_name',
        computing the minimum price and total quantity for each group.

        Parameters:
        ----------
        df : pd.DataFrame
            The input DataFrame containing the data to aggregate.

        Returns:
        -------
        pd.DataFrame
            A DataFrame containing the aggregated data.
        """
        df = df.groupby(self.MARKET_HASH_NAME_KEY)[self.PRICE_KEY, self.QUANTITY_KEY]\
            .agg(price=pd.NamedAgg(column=self.PRICE_KEY, aggfunc='min'),
                 quantity=pd.NamedAgg(column=self.QUANTITY_KEY, aggfunc='sum'))\
            .reset_index()
        return df

    def get_caps(self,
                 mapping: pd.DataFrame,
                 upper_multiplier: float,
                 lower_multiplier: float):
        """
        Derives the caps for each skin in the mapping.

        Parameters:
        ----------
        mapping : pd.DataFrame
            The input DataFrame containing skins and their avg and std dev of
            index share.
        upper_multiplier : float
            The multiplier to use for the upper cap.
        lower_multiplier : float
            The multiplier to use for the lower cap.

        Returns:
        -------
        pd.DataFrame
            Input dataframe with caps added.
        """
        # Get caps for each skin
        mapping = pd.read_csv(self.CSV_PATH, index_col=0)
        mapping['upper_cap_index_share'] = (
            mapping['avg_index_share']
            + upper_multiplier * mapping['std_index_share']
        )
        mapping['lower_cap_index_share'] = (
            mapping['avg_index_share']
            - lower_multiplier * mapping['std_index_share']
        )
        return mapping

    def get_index(self, df: pd.DataFrame, caps: pd.DataFrame):
        """
        Computes the index; given market_hash_name, price, quantity, and caps.

        Parameters:
        ----------
        df : pd.DataFrame
            The input DataFrame containing the data to aggregate.
        caps : pd.DataFrame
            The input DataFrame containing the caps for each skin.

        Returns:
        -------
        float
            The computed index.
        """
        # Get caps
        df = df.merge(caps, on=self.MARKET_HASH_NAME_KEY, how='inner')

        # Get index share
        df['index'] = df[self.PRICE_KEY] * df[self.QUANTITY_KEY]
        sum_index = df['index'].sum()
        df['index_share'] = (df['index'] / sum_index)

        # Apply caps
        valid = df[(df['index_share'] >= df['lower_cap_index_share']) &
                   (df['index_share'] <= df['upper_cap_index_share'])]
        valid_ind = valid['index'].sum()

        # Invalid Entries: Those below lower_cap_index_share
        invalid_lower = df[df['index_share'] < df['lower_cap_index_share']]
        invalid_lower_ind = invalid_lower['lower_cap_index_share'].sum()

        # Invalid Entries: Those above upper_cap_index_share
        invalid_upper = df[df['index_share'] > df['upper_cap_index_share']]
        invalid_upper_ind = invalid_upper['upper_cap_index_share'].sum()

        # Sum capped index shares
        capped_share = invalid_lower_ind + invalid_upper_ind

        # Total index
        index = valid_ind/(1-capped_share)

        return index


if __name__ == '__main__':
    csgo = CSGOSkins()
    data = csgo.get_prices()
    df = csgo.get_prices_df()
    df = csgo.agg_data(df)
    caps = csgo.get_caps(df, upper_multiplier=1, lower_multiplier=2)
    index = csgo.get_index(df, caps)
    print(index)
