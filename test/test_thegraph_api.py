import unittest
from unittest.mock import patch, MagicMock
from apis.thegraph import thegraph_api


class TestBaseGraphQuery(unittest.TestCase):

    @patch('apis.thegraph.thegraph_api.os.getenv', return_value='mock-api-key')
    @patch('apis.thegraph.thegraph_api.requests.post')
    def test_execute_query(self, mock_post, mock_getenv):
        # Setup mock response for the post request
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'mock_data'}
        mock_post.return_value = mock_response

        # Perform the query
        query = 'mock_query'
        base_graph_query = thegraph_api.BaseGraphQuery('mock-subgraph-id')
        response = base_graph_query.execute_query(query)

        # Assertions
        mock_post.assert_called_once()
        self.assertEqual(response, {'data': 'mock_data'})

    @patch('apis.thegraph.thegraph_api.BaseGraphQuery.execute_query')
    def test_check_data_quality(self, mock_execute_query):
        # Setup mock response for the execute_query call
        mock_execute_query.return_value = {
            'data': {
                '_meta': {
                    'block': {'number': 12345678},
                    'hasIndexingErrors': False
                }
            }
        }

        # Perform the data quality check
        base_graph_query = thegraph_api.BaseGraphQuery('mock-subgraph-id')
        # No Exception means data quality check passed
        base_graph_query.check_data_quality(12345670, 10)

        # Test with indexing errors
        mock_execute_query.return_value['data']['_meta']['hasIndexingErrors'] = True
        with self.assertRaises(Exception) as context:
            base_graph_query.check_data_quality(12345670, 10)
        self.assertIn("Subgraph has indexing errors.", str(context.exception))

    @patch('apis.thegraph.thegraph_api.GraphQueryWithPagination.execute_query')
    @patch('apis.thegraph.thegraph_api.GraphQueryWithPagination.extract_data')
    def test_execute_paginated_query(self, mock_extract_data,
                                     mock_execute_query):
        # Setup mock responses
        mock_execute_query.side_effect = [
            {'data': {'mock_data_key': [{'timestamp': '12345'},
                                        {'timestamp': '12346'}]}},
            {'data': {'mock_data_key': []}}  # Empty response to end pagination
        ]
        mock_extract_data.side_effect = lambda x: x['data']['mock_data_key']

        # Perform paginated query
        graph_query_with_pagination = thegraph_api.GraphQueryWithPagination(
            'mock-subgraph-id',
            data_path=['mock_data_key']
        )
        response =\
            graph_query_with_pagination.execute_paginated_query('mock_query')

        # Assertions
        mock_execute_query.assert_called()
        mock_extract_data.assert_called()
        self.assertEqual(response, [{'timestamp': '12345'},
                                    {'timestamp': '12346'}])


if __name__ == '__main__':
    unittest.main()
