from feeds import gauss

Gauss = gauss.Gauss(
	pct = .01,
	vol = 1,
	heartbeat = 10
	)

all_feeds = {'gauss': Gauss}
