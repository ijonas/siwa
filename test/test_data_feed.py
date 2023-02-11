import os
from feeds import data_feed
from feeds.test import test_feed
from datetime import datetime
import constants as c
import unittest
import pandas as pd

Test =  test_feed.Test

class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # if os.path.exists(Test.get_data_dir()):
        ...
        #     os.remove(Test.get_data_dir()) 

    @classmethod
    def tearDownClass(cls):
        os.remove(Test.get_data_dir())#c.TEST_PATH / (Test.NAME + c.DATA_EXT))

    def test_run(self):
        self.assertRaises(NotImplementedError, Test.get_data_point)

    def test_get_data_dir(self):
        self.assertEqual(Test.get_data_dir(), c.DATA_PATH / (Test.NAME + c.DATA_EXT))

    def test_get_last_csv_line(self):
        Test.NAME = 'new_funky_name'
        self.assertIsNone(Test.get_last_csv_line())

        Test.save_data_point(0)
        line = Test.parse_csv_line(Test.get_last_csv_line())
        self.assertEqual(datetime, type(line[0]))
        self.assertEqual(0, line[1])

        Test.save_data_point(1)
        line1 = Test.parse_csv_line(Test.get_last_csv_line())
        self.assertEqual(datetime, type(line[0]))
        self.assertEqual(1, line1[1])

        Test.save_data_point(2)
        line2 = Test.parse_csv_line(Test.get_last_csv_line())
        self.assertEqual(datetime, type(line[0]))
        self.assertEqual(2, line2[1])

    def test_get_most_recently_stored_data_point(self):
        data = Test.get_most_recently_stored_data_point()
        self.assertEqual(Test.NAME, data[c.FEED_NAME])
        self.assertEqual(datetime, type(data[c.TIME_STAMP]))
        self.assertEqual(2, data[c.DATA_POINT])

if __name__ == '__main__':
    unittest.main()

