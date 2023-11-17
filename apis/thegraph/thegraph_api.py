import requests
import os


class BaseGraphQuery:
    GRAPH_API_KEY = 'GRAPH_API_KEY'

    def __init__(self, subgraph_id):
        api_key = os.getenv(self.GRAPH_API_KEY)
        if not api_key:
            raise Exception("GRAPH_API_KEY not found in env variables.")
        self.subgraph_url = f"https://gateway-arbitrum.network.thegraph.com/api/{api_key}/subgraphs/id/{subgraph_id}"  # noqa: E501

    def execute_query(self, query, variables=None,
                      latest_block=None, block_tolerance=None):
        if latest_block is not None:
            self.check_data_quality(latest_block, block_tolerance)
        response = requests.post(self.subgraph_url,
                                 json={'query': query, 'variables': variables})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Query failed with status code "
                            f"{response.status_code}: {response.text}")

    def check_data_quality(self, latest_block, block_tolerance):
        '''
        Check if the data returned by the subgraph is recent.

        Parameters
        ----------
        latest_block : int
            The latest block number on the network.
        block_tolerance : int
            The number of blocks the subgraph data can be behind the latest.

        '''
        query = """
            {
                _meta {
                    block {
                        number
                    }
                    deployment
                    hasIndexingErrors
                }
            }
        """
        if block_tolerance is None:
            raise Exception("Must provide block_tolerance.")
        response = self.execute_query(query)
        if response['data']['_meta']['hasIndexingErrors']:
            raise Exception("Subgraph has indexing errors.")
        block_number = response['data']['_meta']['block']['number']
        if block_number < latest_block - block_tolerance:
            raise Exception("Subgraph data is stale.")


class GraphQueryWithPagination(BaseGraphQuery):
    def __init__(self, subgraph_id, data_path=None):
        super().__init__(subgraph_id)
        self.data_path = data_path or []

    def extract_data(self, response):
        data = response.get('data', {})
        for key in self.data_path:
            data = data.get(key, {})
            if data is None:
                break
        return data

    def execute_paginated_query(self, query, variables=None, page_size=100,
                                latest_block=None, block_tolerance=None):
        if latest_block is not None:
            self.check_data_quality(latest_block, block_tolerance)
        all_data = []
        has_more_pages = True
        variables = variables or {}
        end_time = variables.get('endTime')

        while has_more_pages:
            response = self.execute_query(query, variables)
            page_data = self.extract_data(response)

            if not page_data:
                break  # No more data to fetch

            all_data.extend(page_data)
            last_item = page_data[-1]
            last_timestamp = int(last_item.get('timestamp'))

            # If the last timestamp >= to the end_time, stop fetching
            if end_time and last_timestamp >= end_time:
                break

            # Update startTime for the next page
            variables['startTime'] = last_timestamp

            # Check if we received less data than we asked for.
            # Indicates this is the last page.
            if len(page_data) < page_size:
                has_more_pages = False

        return all_data
