from feeds.gauss import gauss
from feeds import test_feed

Test = test_feed.Test
Gauss = gauss.Gauss

#NOTE: this is a dict of all feed classes that SIWA can run, keyed by feed name
#     this is used in endpoint.py to route requests to the correct feed
#
#TO ENABLE OR DISABLE A FEED, ADD OR REMOVE IT FROM THIS DICT  
all_feeds = {
    'gauss': Gauss, 
    'test': Test
    }
