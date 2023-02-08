import os
import sys
import cmd2
import logging
import argparse
import threading
import constants as c
from datetime import datetime, timezone
from all_feeds import all_feeds

#TODO:

# all_feeds = []
all_threads = {}

class Siwa(cmd2.Cmd):
    '''
    '''
    prompt = '\nSIWA> '

    def __init__(self):
        super().__init__()
        # Make maxrepeats settable at runtime
        self.maxrepeats = 1
        self.init_time = datetime.now(timezone.utc)


    def do_status(self, args: cmd2.Statement):
        #if -v then shows params too

        self.poutput(c.init_time_message(self))

        for feed in all_feeds.values():
            self.poutput(c.status_message(feed))


    # start_args_parse = cmd2.Cmd2ArgumentParser()
    # start_args_parse.add_argument('--feed', help='Specific feed to start')
    # @cmd2.with_argparser(start_args_parse)
    def do_start(self, args: cmd2.Statement):

        feeds = all_feeds.values()
        if args:
            feeds = [all_feeds[f] for f in args.arg_list]

        for feed in feeds:
            feed.ACTIVE = True
            feed.START_TIME = datetime.now(timezone.utc)

            self.poutput(c.start_message(feed))

            thread = threading.Thread(target=feed.run)
            thread.start()
            all_threads[feed.NAME] = thread


    # stop_args_parse = cmd2.Cmd2ArgumentParser()
    # start_args_parse.add_argument('--feed', help='Specific feed to stop')
    # @cmd2.with_argparser(stop_args_parse)
    def do_stop(self, args: cmd2.Statement):

        feeds = all_feeds.values()
        if args:
            feeds = [all_feeds[f] for f in args.arg_list]

        for feed in feeds:
            feed.ACTIVE = False
            self.poutput(c.stop_message(feed))



if __name__ == '__main__':
    sys.exit(Siwa().cmdloop())


