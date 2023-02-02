from feeds import gauss

Gauss = gauss.Gauss(
	pct = .01,
	vol = 1,
	)

print(f'data dir: {Gauss.data_dir}')

all_feeds = {'gauss': Gauss}
