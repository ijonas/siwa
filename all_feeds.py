from feeds.gauss import gauss
from feeds.test import test_feed

Test = test_feed.Test
Gauss = gauss.Gauss

all_feeds = {'gauss': Gauss, 'test':Test}
