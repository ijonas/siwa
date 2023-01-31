from gauss import gauss
import daemon
import unittest
import pandas as pd

class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ...

    @unittest.skip('')
    def test_daemon(self):
        with daemon.DaemonContext():
            gauss.run()


    def test_daemon2(self):
        breakpoint()
        app = gauss.Gaussian()
        daemon_runner = runner.DaemonRunner(app)
        daemon_runner.do_action()

if __name__ == '__main__':
    unittest.main()

