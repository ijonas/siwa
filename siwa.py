import os
import sys
import cmd2
import logging
import argparse
import threading
import constants as c
from datetime import datetime, timezone
from all_feeds import all_feeds

import endpoint
endpoint_thread = threading.Thread(target=endpoint.run, daemon=True)
endpoint_thread.start()

datafeed_threads = {}

class Siwa(cmd2.Cmd):
    ''' siwa CLI: allows user to start/stop datafeeds, list feed statuses '''
    prompt = '\nSIWA> '

    def __init__(self):
        super().__init__()
        # Make maxrepeats settable at runtime
        self.maxrepeats = 1
        self.init_time = datetime.now(timezone.utc)


    def do_status(self, args: cmd2.Statement):
        '''show status (active, inactive) for all datafeeds,
        if debug enabled, also show status of threads; 
        inactive datafeeds merely sleep, they do not close their threads'''
        #if -v then shows params too
        self.poutput(c.init_time_message(self))

        for feed in all_feeds.values():
            self.poutput(c.status_message(feed))

        if c.DEBUG:
            print('\n\n--- DEBUG INFO ---',
                '\n    datafeed threads running: ',
                            threading.active_count()-6, 
                            #-2 because main(x1) and endpoint(x5) threads not included
                '\n    total threads (incl. 1 main + 5 endpoint): ', 
                            threading.active_count(),
                '\n    feeds threads running: ', datafeed_threads.keys())

    def do_start(self, args: cmd2.Statement):
        '''start specific feed if specified, else start all feeds;
        create new thread for feed if none extant'''
        if args:
            #start specific feed, if given
            feeds = [all_feeds[f] for f in args.arg_list]
        else:
            #else start all feeds
            feeds = all_feeds.values()

        for feed in feeds:
            #(re)activate feed / allow it to start or resume processing
            feed.ACTIVE = True
            feed.START_TIME = datetime.now(timezone.utc)

            #print datafeed startup message to CLI
            self.poutput(c.start_message(feed))

            #create new thread *only if* one doesn't already exist
            if not feed.NAME in datafeed_threads:
                thread = threading.Thread(target=feed.run)
                thread.start()
                datafeed_threads[feed.NAME] = thread

    def do_stop(self, args: cmd2.Statement):
        '''stop datafeed processing
        (thread remains running in case we want to re-activate)'''
        if args:
            #stop specific feed, if given
            feeds = [all_feeds[f] for f in args.arg_list]
        else:
            #else stop all feeds
            feeds = all_feeds.values()

        for feed in feeds:
            feed.ACTIVE = False
            self.poutput(c.stop_message(feed))

if __name__ == '__main__':
    sys.exit(Siwa().cmdloop())