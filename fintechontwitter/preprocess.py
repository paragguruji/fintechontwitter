# -*- coding: utf-8 -*-
"""
Created on Wed Apr 05 17:53:34 2017

@author: Parag
"""

import pandas
import re
import logging
from datetime import datetime
from collections import Counter
from fintechontwitter import DATA_FILE, DATE_FORMAT, PREPROCESSED

logger = logging.getLogger('fintechontwitter')

key_sequence = ['urls', 'html_tags', 'user_mentions', 'hashtags', 'emoticons',
                'numbers', 'words', 'characters', 'misc']

features = ['user_mentions', 'hashtags', 'emoticons',
            'plaintext', 'words', 'rt']

regex_strings = {
        "emoticons": r"""(?:[%s][%s]?[%s])""" % tuple(map(re.escape,
                                                          [r":;8X=",
                                                           r"-oO",
                                                           r"()[]\|DPpO"])),
        "html_tags": r'<[^>]+>',
        "user_mentions": r'(?:@[\w_]+)',
        "hashtags": r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",
        "urls": r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|\
                (?:%[0-9a-fA-F][0-9a-fA-F]))+",
        "numbers": r'(?:(?:\d+,?)+(?:\.?\d+)?)',
        "words": r"(?:[a-zA-Z0-9]+(?:[-'_]*[a-zA-Z0-9]+)+)",
        "characters": r'(?:[\w])',
        "misc": r'(?:[^\w ]+)'}


tokens_re = re.compile(r'(' +
                       r'|'.join([regex_strings[k] for k in key_sequence]) +
                       r')',
                       re.VERBOSE)
plaintext_re = re.compile(r'(' +
                          r'|'.join([regex_strings[k]
                                     for k in
                                     ['numbers', 'hashtags', 'user_mentions',
                                      'words', 'characters']]) +
                          r')')
regex = {key: re.compile(r'^' + regex_strings[key] + '$', re.VERBOSE)
         for key in key_sequence}

non_decimal = re.compile(r'[^\d.]+')


def parse_followers(x):
    if isinstance(x, int) or isinstance(x, float):
        return x
    else:
        try:
            ret = non_decimal.sub('', x)
        except TypeError:
            ret = ''
    return ret


def parse_date(date_str):
    dt = date_str[:20] + date_str[26:]
    tz = date_str[20:25]
    return pandas.to_datetime(dt, format=DATE_FORMAT, errors='raise') + \
        datetime.timedelta(minutes=((60*int(tz[1:3]) + int(tz[3:5])) *
                                    (-1 if tz[0] == '-' else 1)))


def preprocess(s):
    s = s.replace('\N',
                  ' ').replace('\n',
                               ' ').replace('\t',
                                            ' ').replace('\T', ' ').strip()
    while('  ' in s):
        s = s.replace('  ', ' ')
    tokens = tokens_re.findall(s)
    plaintext = s
    classified_tokens = {}
    classified_tokens['hashtags'] = [token.upper() for token in tokens
                                     if regex['hashtags'].search(token)]
    classified_tokens['user_mentions'] = [token for token in tokens if
                                          regex['user_mentions'].search(token)]
    classified_tokens['emoticons'] = [token for token in tokens
                                      if regex['emoticons'].search(token)]
    classified_tokens['words'] = Counter([token for token in tokens
                                          if regex['words'].search(token)])

    plaintext = re.sub(regex_strings['urls'], "", plaintext)
    plaintext = re.sub(regex_strings['html_tags'], "", plaintext)
    plaintext = ' '.join(plaintext_re.findall(plaintext))

    classified_tokens['plaintext'] = plaintext.replace('#', '')
    classified_tokens['rt'] = s.startswith('RT')
    return classified_tokens


def featureGen(tweet):
    feature_data = preprocess(tweet['tweet'])
    return pandas.Series([feature_data[key] for key in features])


def load_frame():
    df = pandas.read_pickle(DATA_FILE)
    logger.info("loaded " + ("processed" if PREPROCESSED else "raw") + " data")
    if not PREPROCESSED:
        df.loc[:, 'followers'] = \
            pandas.to_numeric(df['followers'].map(parse_followers),
                              errors='raise',
                              downcast='integer')
        logger.info("Follower count transformed")
        df.loc[:, 'date'] = df['date'].map(parse_date)
        logger.info("Dates transformed...")
        logger.info("Preprocessing and generating features...")
        newcols = df.apply(featureGen, axis=1)
        newcols.columns = features
        logger.info("Adding new features to dataframe...")
        return df.join(newcols)
    else:
        return df
