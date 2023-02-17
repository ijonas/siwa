#stdlib
import os
import sys
import logging
import argparse
import threading
import time
from datetime import datetime, timezone

#third party
import cmd2

#our stuff
from all_feeds import all_feeds
import constants as c
import endpoint

datafeed_threads = {}

endpoint_thread = threading.Thread(target=endpoint.run, daemon=True, kwargs={'all_feeds':all_feeds})
endpoint_thread.start()

class Siwa(cmd2.Cmd):
    ''' siwa CLI: allows user to start/stop datafeeds, list feed statuses '''
    prompt = '\nSIWA> '

    def __init__(self):
        super().__init__()
        # Make maxrepeats settable at runtime
        self.maxrepeats = 1
        self.init_time = time.time()
        self.debug = c.DEBUG
        if self.debug:
            self.poutput(':::DEBUG MODE ENABLED:::')

    def do_status(self, args: cmd2.Statement):
        '''show status (active, inactive) for all datafeeds,
        if debug enabled, also show status of threads; 
        inactive datafeeds merely sleep, they do not close their threads'''
        #if -v then shows params too

        self.poutput(c.init_time_message(self))

        for feed in all_feeds.values():
            self.poutput(c.status_message(feed))
            self.poutput(f'{feed.NAME} deque len: {len(feed.DATAPOINT_DEQUE)}')

        if c.DEBUG:
            threadcount = threading.active_count()
            datafeed_threadcount = threading.active_count()-1 -1 -c.WEBSERVER_THREADS
            endpoint_threadcount = 1+c.WEBSERVER_THREADS
            self.poutput(f'''
                --- THREAD DEBUG INFO ---
                datafeed threads running: {datafeed_threadcount}
                total threads: {threadcount} (1 main, {endpoint_threadcount} endpoint, and {datafeed_threadcount} feeds)
                feeds threads running: {list(datafeed_threads.keys()) or '[none]'}''')

    def do_start(self, args: cmd2.Statement):
        '''start specified feed, if none specified start all;
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
            feed.START_TIME = time.time()
            
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

    def do_quit(self,args: cmd2.Statement):
        """Exit the application"""
        self.poutput('quitting; waiting for heartbeat timeout')
        for feed in all_feeds.values(): feed.ACTIVE=False
        return True

if __name__ == '__main__':
    sys.exit(Siwa().cmdloop())