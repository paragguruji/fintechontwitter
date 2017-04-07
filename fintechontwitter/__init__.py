# -*- coding: utf-8 -*-
"""
Created on Tue Apr 04 16:34:13 2017

@author: Parag
"""
import datetime
import os
import logging
import sys
import pandas
import re

PICKLE_FILENAME = "FinTech_cleaned.pkl"
LOG_FILENAME = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".log"

repo_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

log_dir_path = os.path.join(repo_path, "log")
if not os.path.isdir(log_dir_path):
    os.makedirs(log_dir_path)

log_file_path = os.path.join(log_dir_path, LOG_FILENAME)
if not os.path.isfile(log_file_path):
    open(log_file_path, "w").close()

# create logger
logger = logging.getLogger('fintechontwitter')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(log_file_path)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level ERROR
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

data_dir_path = os.path.join(repo_path, "data")
data_file_path = os.path.join(data_dir_path, PICKLE_FILENAME)
if not os.path.isfile(data_file_path):
    logger.exception("data file not found - %s", data_file_path)
    for handler in logger.handlers:
        handler.close()
    sys.exit(1)

DATAFRAME = pandas.read_pickle(data_file_path)
DATAFRAME.loc[:, 'followers'] = pandas.to_numeric(DATAFRAME['followers'],
                                                  errors='coerce',
                                                  downcast='integer')
DATAFRAME.loc[:, 'date'] = pandas.to_datetime(DATAFRAME['date'],
                                              errors='coerce',
                                              infer_datetime_format=True)
DATAFRAME['retweet'] = DATAFRAME['tweet'].map(lambda x: x.startswith("RT"))
DATAFRAME['tokens '] = DATAFRAME['tweet'].map(lambda x: re.sub(r"http\S+", "", x))
DATAFRAME['hashtags'] = DATAFRAME['text'].map(lambda x: pandas.Series(re.findall(r"#(\w+)", x)))
