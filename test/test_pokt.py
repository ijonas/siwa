import unittest
import constants as c
from datetime import datetime, timedelta
from pokt import Pokt, Translucent


class TestTask(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     cls.pokt = Pokt

    def test_gauss_answer(self):
        gauss = Translucent.gauss_test
        ans = gauss.functions.latestAnswer().call()
        self.assertTrue(isinstance(ans, int))

    @classmethod
    def tearDownClass(cls):
        ...

if __name__ == '__main__':
    unittest.main()

