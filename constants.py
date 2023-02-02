import os
from pathlib import Path

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

DATA_DIR = 'data'
LOGGING_FILE = 'data_feeds.log'
DATEFORMAT = '%Y-%m-%d %H:%M:%S.%f, %z'
DATA_EXT = '.csv'

PROJECT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
DATA_PATH = PROJECT_PATH / DATA_DIR
LOGGING_PATH = DATA_PATH / LOGGING_FILE

