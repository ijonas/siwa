import os
import time
import logging
import pandas as pd
import typing as tp
import constants as c
from threading import Lock
from datetime import datetime, timezone
from dataclasses import dataclass
 
# logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s:%(thread)d - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter
logger = logging.getLogger('SQLLogger')
logger.setLevel(logging.INFO)
logging.basicConfig(
        filename=c.LOGGING_PATH,
        filemode='a+',
        format=c.LOGGING_FORMAT
        )


@dataclass
class DataFeed:
    ''' The base-level implementation for all data feeds, which should inherit from DataFeed and implement the get_data_point method as required.
    '''

    #NOTE: all feeds must define these class-level attributes
    NAME: str
    ID: int
    HEARTBEAT: int              #in seconds
    START_TIME: datetime
    ACTIVE: bool = False
    COUNT: int = 0              #number of data points served since starting
    DATA_KEYS = (c.FEED_NAME, c.TIME_STAMP, c.DATA_POINT)


    @classmethod
    def get_data_dir(cls):
        return c.DATA_PATH / (cls.NAME + c.DATA_EXT)


    @classmethod
    def run(cls):
        while cls.ACTIVE:
            dp = cls.get_data_point(cls)
            logging.info('\nNext data point for {cls.NAME}: {dp}\n')
            cls.save_data_point(dp)
            cls.COUNT += 1
            time.sleep(cls.HEARTBEAT)

    @classmethod
    def get_data_point(cls):
        raise NotImplementedError

    @classmethod
    def save_data_point(cls, dp):
        with Lock():
            with open(cls.get_data_dir(), 'a+') as datafile:
                datafile.write(cls.format_data(dp))

    @classmethod
    def get_last_csv_line(cls):
        if not os.path.exists(cls.get_data_dir()):
            return None
        
        with open(cls.get_data_dir(), 'rb') as datafile:
            datafile.seek(-2, os.SEEK_END)
            while datafile.read(1) != f'{c.LINE_START}'.encode(): #needs to be in bytes
                datafile.seek(-2, os.SEEK_CUR)

            return datafile.readline().decode("utf-8").replace(c.LINE_START, '')

    @classmethod
    def parse_csv_line(cls, line):
        line = line.split(',')
        timestamp = datetime.strptime(line[0], c.DATEFORMAT)
        data_point = float(line[1]) #TODO: are floats OK? decimal type needed?
        return timestamp, data_point

    @classmethod
    def line_to_dict(cls, line):
        return dict(zip(cls.DATA_KEYS, line)) 

    @classmethod
    def get_most_recently_stored_data_point(cls):
        '''return most recently stored-to-disk data point;
        returns dict of {feedname, timestamp, datapoint}'''
        line = (cls.NAME,) + cls.parse_csv_line(cls.get_last_csv_line())
        return dict(zip(cls.DATA_KEYS, line))

        # return cls.line_to_dict(
        # data_point = None

        # try:
        #     with open(cls.get_data_dir(), 'r') as datafile:
        #         try:
        #             #find only last line of CSV, which may be huge
        #             datafile.seek(-2, os.SEEK_END)
        #             while datafile.read(1) != b'\n':
        #                 datafile.seek(-2, os.SEEK_CUR)

        #         except OSError:
        #             # handle case csv file is new and has only 1 line
        #             datafile.seek(0)

        #         last_csv_line = datafile.readline()
        #         if last_csv_line:
        #             # if csv file not blank:
        #             data_values = last_csv_line.split(', ')
        #             data_point = {'feedname':cls.NAME,
        #                         #output same format;
        #                         #csv would be easier to parse if no comma in c.DATEFORMAT
        #                         'timestamp':', '.join(data_values[:2]),

        #                         #alternatively...
        #                         #'timestamp':datetime.strptime(', '.join(data_values[:2]), c.DATEFORMAT),
        #                         #TODO: are floats OK? decimal type needed?
        #                         'data_point':float(data_values[2])}
        #     return data_point
        # except Exception as e:
        #     #if file doesn't exist:
        #     return data_point

    @staticmethod
    def format_data(dp):
        timenow =  datetime.now(timezone.utc)
        strtime = timenow.strftime(c.DATEFORMAT)
        return f'{c.LINE_START}{strtime},{dp},\n'
