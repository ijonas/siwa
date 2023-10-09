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
    prices_endpoint = 'api/v1/prices'
    price_histories_endpoint = 'api/v1/price-histories'
    price_histories_rpm = 20  # Max requests per min for histories

    def __init__(self, base_url='https://csgoskins.gg/'):
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
        self.api_key = get_api_key('CSGO')
        self.headers = {
            'Authorization': "Bearer " + self.api_key,
            'Content-Type': 'application/json'
        }

    def get_prices(self, range='current', agg="max"):
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
        url = self.base_url + self.prices_endpoint
        payload = {
            "range": range,
            "aggregator": agg
        }

        response = requests.request('GET', url,
                                    headers=self.headers, json=payload)
        data = response.json()
        return data

    def get_prices_df(self, range='current', agg='max'):
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
            data['data'], record_path='prices', meta='market_hash_name'
        )
        df.price = df.price/100  # API gives prices in USD cents
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
        df = df.groupby('market_hash_name')['price', 'quantity']\
            .agg(price=pd.NamedAgg(column='price', aggfunc='min'),
                 quantity=pd.NamedAgg(column='quantity', aggfunc='sum'))\
            .reset_index()
        return df

    def get_caps(self,
                 mapping,
                 upper_multiplier,
                 lower_multiplier):
        """
        Derives the caps for each skin in the mapping.

        Parameters:
        ----------
        mapping : pd.DataFrame
            The input DataFrame containing skins and their avg and std dev of
            index share.

        Returns:
        -------
        pd.DataFrame
            Input dataframe with caps added.
        """
        # Get caps for each skin
        mapping = pd.read_csv('apis/csgo/csgo_mapping.csv')
        mapping['upper_cap_index_share'] = (
            mapping['avg_index_share']
            + upper_multiplier*mapping['std_index_share']
        )
        mapping['lower_cap_index_share'] = (
            mapping['avg_index_share']
            - lower_multiplier*mapping['std_index_share']
        )
        return mapping

    def get_index(self, df, caps):
        # Get caps
        df = df.merge(caps, on='market_hash_name', how='inner')

        # Get index share
        df['index'] = df['price'] * df['quantity']
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
        breakpoint()

        return index


if __name__ == '__main__':
    csgo = CSGOSkins()
    data = csgo.get_prices()
    df = csgo.get_prices_df()
    df = csgo.agg_data(df)
    caps = csgo.get_caps(df, upper_multiplier=1, lower_multiplier=2)
    index = csgo.get_index(df, caps)
    print(index)
    breakpoint()
