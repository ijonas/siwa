import os
from pathlib import Path

DEBUG = True #show debug messages in CLI

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
NOUNDERLINE = '\033[0m'

DATA_DIR = 'data'
LOGGING_FILE = 'data_feeds.log'
DATEFORMAT = '%Y-%m-%d %H:%M:%S.%f, %z'
DATA_EXT = '.csv'

PROJECT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
DATA_PATH = PROJECT_PATH / DATA_DIR
LOGGING_PATH = DATA_PATH / LOGGING_FILE
LOGGING_FORMAT = ('%(asctime)s:%(thread)d - %(name)s - %(levelname)s - %(message)s')


def start_message(feed):
    return f'\n{HEADER}Starting {UNDERLINE}{feed.NAME}{NOUNDERLINE} {HEADER}data feed!{ENDC}'

def stop_message(feed):
    return f'\n{OKCYAN}Shutting down {UNDERLINE}{feed.NAME}{NOUNDERLINE} {OKCYAN}...{ENDC}'

def init_time_message(cls):
    return f'\nSiwa init time: {cls.init_time.strftime(DATEFORMAT)}'

get_color = lambda x: OKGREEN if x else FAIL
get_word = lambda x: '' if x else 'not '
get_time = lambda feed: f'since {feed.START_TIME.strftime(DATEFORMAT)}' if hasattr(feed, 'START_TIME') else ''
def status_message(feed):
    x = feed.ACTIVE
    return f'{get_color(x)}{feed.NAME}{ENDC} with id {feed.ID} is {get_word(x)}active, with {feed.COUNT} data points served {get_time(feed)}'
