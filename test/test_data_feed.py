from feeds import data_feed
import constants as c
import unittest
import pandas as pd

class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        name = 'testy'
        id_ = 100
        heartbeat = 1
        start_time = 'now'
        cls.feed = data_feed.DataFeed(name, id_, heartbeat, start_time)

    def test_run(self):
        self.assertRaises(NotImplementedError, self.feed.get_data_point)

    def test_get_data_dir(self):
        self.assertRaises(AttributeError, self.feed.get_data_dir)


if __name__ == '__main__':
    unittest.main()

