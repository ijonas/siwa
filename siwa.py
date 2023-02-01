#!/usr/bin/env python3
"""guideline

Usage:
siwa.py start <feed>
siwa.py stop <feed>
siwa.py feeds
siwa.py display [<task>] [-d <date>]
siwa.py view <task>
siwa.py network

Options:
-d <date>, --date <date>    Date in this format: 2021-01-21
-h, --help                  Show this screen
"""

#TODO:

import os
import logging
import threading
from docopt import docopt
from all_feeds import all_feeds


if __name__ == '__main__':
    kwargs = docopt(__doc__, version='siwa 0.1')
    print(kwargs)

    #Display all enabled feeds with args
    if kwargs['feeds']:
        ...

    if kwargs['start']:
        feed_name = kwargs['<feed>']
        Feed = all_feeds[feed_name]

        thread = threading.Thread(
                target=Feed.get_data_point(),
                daemon=True)
        thread.start()


