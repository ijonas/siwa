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
        #up and down feeds
        #how long up
        #how many data points served
        #if -v then shows params too
        get_color = lambda x: c.OKGREEN if x else c.FAIL
        get_word = lambda x: '' if x else 'not '

        for feed in all_feeds.values():
            x = feed.ACTIVE
            self.poutput(
                    f'\nSiwa init time: {self.init_time.strftime(c.DATEFORMAT)}\n{get_color(x)}{feed.NAME}{c.ENDC} with id {feed.ID} is {get_word(x)}active, with {feed.COUNT} data points served since {feed.START_TIME.strftime(c.DATEFORMAT)}\n'
                )


    start_args_parse = cmd2.Cmd2ArgumentParser()
    start_args_parse.add_argument('feed', help='Specific feed to start')
    start_args_parse.add_argument('-p', '--print', action='store_true', help='Print the output of the data feed to console')
    @cmd2.with_argparser(start_args_parse)
    def do_start(self, args: cmd2.Statement):
        Feed = all_feeds[args.feed]
        Feed.ACTIVE = True
        Feed.START_TIME = datetime.now(timezone.utc)
        self.poutput(f'\n{c.HEADER}Starting {Feed.NAME} data feed!{c.ENDC}')

        thread = threading.Thread(
                target=Feed.run,
                kwargs={'printdata':args.print}
                )

        thread.start()
        all_threads[args.feed] = thread


    stop_args_parse = cmd2.Cmd2ArgumentParser()
    stop_args_parse.add_argument('feed', help='Specific feed to stop')
    @cmd2.with_argparser(stop_args_parse)
    def do_stop(self, args: cmd2.Statement):
        feed = all_feeds[args.feed]
        feed.ACTIVE = False
        self.poutput(f'\n{c.OKCYAN}Shutting down {feed.NAME}...{c.ENDC}')


if __name__ == '__main__':
    sys.exit(Siwa().cmdloop())


