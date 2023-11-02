from feeds.gauss import gauss
from feeds.crypto_indices import mcap1000, memecoins
from feeds.csgo import csgo_index
from feeds.evm import eth_burn_rate
from feeds.stablecoins import stablecoins as s
from feeds import test_feed
from feeds.twitter import twitter

Test = test_feed.Test
Gauss = gauss.Gauss
MCAP1000, MemeCoins = mcap1000.MCAP1000, memecoins.MemeCoins
USDC, BUSD, Tether, Dai = s.USDC, s.BUSD, s.Tether, s.Dai
Twitter = twitter.Twitter
csgo_index = csgo_index.CSGOIndex
eth_burn_rate = eth_burn_rate.EthBurnRate

#NOTE: this is a dict of all feed classes that SIWA can run, keyed by feed name
#     this is used in endpoint.py to route requests to the correct feed
#
#TO ENABLE OR DISABLE A FEED, ADD OR REMOVE IT FROM THIS DICT  
all_feeds = {
    # Gauss.NAME: Gauss, 
    Test.NAME: Test,
    MCAP1000.NAME: MCAP1000,
    MemeCoins.NAME: MemeCoins,
    USDC.NAME: USDC, 
    BUSD.NAME: BUSD,
    Tether.NAME: Tether,
    Dai.NAME: Dai,
    Twitter.NAME: Twitter,
    csgo_index.NAME: csgo_index,
    eth_burn_rate.NAME: eth_burn_rate
    }
