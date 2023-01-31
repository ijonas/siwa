#!/usr/bin/env python3
"""guideline

Usage:
siwa.py start <feed>
siwa.py stop <feed>

siwa.py display [<task>] [-d <date>]

siwa.py view <task>
siwa.py network

Options:
-d <date>, --date <date>    Date in this format: 2021-01-21
-h, --help                  Show this screen
"""

#TODO:

import os
import docopt
import daemon
import logging


if __name__ == '__main__':
    kwargs = docopt(__doc__, version='siwa 0.1')

        #Print current goals
        if kwargs['start']:
            ...

