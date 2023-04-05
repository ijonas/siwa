import unittest
import numpy as np
import pandas as pd
import constants as c
from feeds.gauss import gauss
from feeds.gauss import random_feed as rf
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

    @unittest.skip('exploration')
    def test_random_feed(self):
        F = self.feed
        for i in range(2000000):
            F.update(pct=.01)
        plt.plot(F.history)
        plt.show()

    def test_gauss_get_data_dir(self):
        self.assertTrue(self.gauss.get_data_dir() == c.DATA_PATH / (self.gauss.NAME + c.DATA_EXT))

    def test__generate_data_point(self):
        data = gauss.TestClass._generate_data_points(10, 100)
        self.assertListEqual(data, [101.76405234596767, 102.17126853695666, 103.17125755097054, 105.48321524496086, 107.45317545953522, 106.40305934454439, 107.41398248726978, 107.25140368205567, 107.14070001464258, 107.58061812386899])

    def test__prep_data(self):
        data = gauss.TestClass._generate_data_points(1000, 100)
        data = gauss.TestClass._prep_data(data)

    # @unittest.skip('for saving test data')
    def test_make_data(self):
        data = pd.read_csv(c.DATA_PATH / 'ETH-USD_2022-01-01-00-00_2022-03-01-00-00_300secs')
        l = len(data) #in 300 sec intervals
        n = int(l * 300)
        for p in [.01, .02, .03]:
            for v in [1, 2, 3]:
                for h in [10, 30, 60]:
                    print(f'doing {p} {v} {h}')
                    g = gauss.TestClass(heartbeat=h, percent=p, volatility=v)
                    gdata =  g._generate_data_points(n, 100)
                    gdata = g._prep_data(gdata)
                    gdata.to_csv(c.DATA_PATH / f'GAUSS_{g.HEARTBEAT}_{g.VOLATILITY}_{g.PERCENT}_.1.csv')


if __name__ == '__main__':
    unittest.main()
    # t = TestConstants
    # t.test_axial_doppler
