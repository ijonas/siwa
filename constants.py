import os, datetime
from pathlib import Path

DEBUG = True #show debug messages in CLI
WEBSERVER_THREADS = 1

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
TEST_DIR = 'test'
LOGGING_FILE = 'data_feeds.db'
DATEFORMAT = '%Y-%m-%d %H:%M:%S.%f %z'
DATA_EXT = '.csv'
LINE_START = '>'

FEED_NAME = 'feed_name'
DATA_POINT = 'data_point'
TIME_STAMP = 'time_stamp'

PROJECT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
DATA_PATH = PROJECT_PATH / DATA_DIR
TEST_PATH = PROJECT_PATH / TEST_DIR
LOGGING_PATH = DATA_PATH / LOGGING_FILE
LOGGING_FORMAT = ('%(asctime)s:%(thread)d - %(name)s - %(levelname)s - %(message)s')

def start_message(feed):
    return f'\n{HEADER}Starting {UNDERLINE}{feed.NAME}{NOUNDERLINE} {HEADER}data feed!{ENDC}'

def stop_message(feed):
    return f'\n{OKCYAN}Shutting down {UNDERLINE}{feed.NAME}{NOUNDERLINE} {OKCYAN}...{ENDC}'

def init_time_message(cls):
    return f'\nSiwa init time: {datetime.datetime.fromtimestamp(cls.init_time).strftime(DATEFORMAT)}'

get_color = lambda x: OKGREEN if x else FAIL
get_word = lambda x: '' if x else 'not '

def get_starttime_string(feed):
    if (hasattr(feed, 'START_TIME') and feed.START_TIME):
        #ensure START_TIME exists and is not None before trying to convert
        dt_from_timestamp = datetime.datetime.fromtimestamp(feed.START_TIME)
        human_readable_time_str = dt_from_timestamp.strftime(DATEFORMAT)
        return f'{human_readable_time_str}'
    else:
        #if START_TIME not initialized (i.e. because "start gauss" not issued yet)
        #(e.g. when calling `status` command before having ever started a feed)
        return f'[NEVER]'

def status_message(feed):
    x = feed.ACTIVE
    return f'{get_color(x)}{feed.NAME}{ENDC} with id {feed.ID} is {get_word(x)}active, with {feed.COUNT} data points served since {get_starttime_string(feed)}'
