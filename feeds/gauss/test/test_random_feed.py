import unittest
import pandas as pd
import random_feed as rf
import numpy as np
import matplotlib.pyplot as plt

#NOTE: Goals are to make sure percent functionality works, discover edge cases, discover long-term properties of data

class TestRandomFeed(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        vol = 1
        px = .0001
        np.random.seed(0)
        cls.Feed = rf.RandomFeed(vol, px)

    def test_new_timesheet(self):
        F = self.Feed
        for i in range(2000000):
            F.update(pct=.01)
        plt.plot(F.history)
        plt.show()



if __name__ == '__main__':
    unittest.main()
    # t = TestConstants
    # t.test_axial_doppler
