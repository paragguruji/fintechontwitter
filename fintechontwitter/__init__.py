# -*- coding: utf-8 -*-
"""
Created on Tue Apr 04 16:34:13 2017

@author: Parag
"""
import datetime
import os
import logging
import sys

PICKLE_FILENAME = "FinTech_cleaned.pkl"
PROCESSED_PICKLE_FILENAME = "processed_data.pkl"
LOG_FILENAME = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".log"
CONF_FILENAME = "local.env"
DATE_FORMAT = '%a %b %d %H:%M:%S %Y'

repo_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

log_dir_path = os.path.join(repo_path, "log")
if not os.path.isdir(log_dir_path):
    os.makedirs(log_dir_path)

log_file_path = os.path.join(log_dir_path, LOG_FILENAME)
if not os.path.isfile(log_file_path):
    open(log_file_path, "w").close()

conf_dir_path = os.path.join(repo_path, "conf")
if not os.path.isdir(conf_dir_path):
    os.makedirs(conf_dir_path)

conf_file_path = os.path.join(conf_dir_path, CONF_FILENAME)


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
DATA_FILE = os.path.join(data_dir_path, PROCESSED_PICKLE_FILENAME)
if not os.path.isfile(DATA_FILE):
    DATA_FILE = os.path.join(data_dir_path, PICKLE_FILENAME)
    if not os.path.isfile(DATA_FILE):
        logger.exception("data file not found - %s", DATA_FILE)
        for handler in logger.handlers:
            handler.close()
        sys.exit(1)

PREPROCESSED = DATA_FILE.endswith(PROCESSED_PICKLE_FILENAME)
