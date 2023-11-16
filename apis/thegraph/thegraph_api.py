import requests
import os


class BaseGraphQuery:
    GRAPH_API_KEY = 'GRAPH_API_KEY'

    def __init__(self, subgraph_id):
        api_key = os.getenv(self.GRAPH_API_KEY)
        if not api_key:
            raise Exception("The Graph API key not found in env variables.")
        self.subgraph_url = f"https://gateway-arbitrum.network.thegraph.com/api/{api_key}/subgraphs/id/{subgraph_id}"  # noqa: E501

    def execute_query(self, query, variables=None):
        response = requests.post(self.subgraph_url,
                                 json={'query': query, 'variables': variables})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Query failed with status code "
                            f"{response.status_code}: {response.text}")


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
