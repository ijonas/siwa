import os
import sys
import cmd2
import logging
import threading
from docopt import docopt
from all_feeds import all_feeds


#TODO:


class Siwa(cmd2.Cmd):
    '''
    '''

    def do_hello_world(self, _: cmd2.Statement):
        self.poutput('Hello World')


    def do_start(self, x: cmd2.Statement):
        self.poutput(f'{x} Hello World')

if __name__ == '__main__':
    c = Siwa()
    sys.exit(c.cmdloop())

if __name__ == '__main__':
    kwargs = docopt(__doc__, version='siwa 0.1')
    # print(kwargs)

    #Display all enabled feeds with args
    if kwargs['feeds']:
        ...

    if kwargs['start']:
        feed_name = kwargs['<feed>']
        Feed = all_feeds[feed_name]
        Feed.ACTIVE = True

        printdata = kwargs.get('--print', False)
        thread = threading.Thread(
                target=Feed.run,
                kwargs={'printdata':printdata}
                )

        thread.start()



    if kwargs['stop']:
        feed_name = kwargs['<feed>']
        Feed = all_feeds[feed_name]
        Feed.ACTIVE = False



