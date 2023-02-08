import gauss
import unittest
import numpy as np
import pandas as pd
import random_feed as rf
import matplotlib.pyplot as plt

#NOTE: Goals are to make sure percent functionality works, discover edge cases, discover long-term properties of data

class TestGauss(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        np.random.seed(0)

        vol = 1
        px = .0001
        cls.feed = rf.RandomFeed(vol, px)

        cls.gauss = gauss.Gauss

    unittest.skip('exploration')
    def test_random_feed(self):
        F = self.feed
        for i in range(2000000):
            F.update(pct=.01)
        plt.plot(F.history)
        plt.show()

    def test_gauss_get_data_dir(self):
        self.assertTrue(self.gauss.get_data_dir() == c.DATA_PATH / (self.gauss.NAME + c.DATA_EXT))


if __name__ == '__main__':
    unittest.main()
    # t = TestConstants
    # t.test_axial_doppler
