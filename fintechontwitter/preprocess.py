# -*- coding: utf-8 -*-
"""
Created on Wed Apr 05 17:53:34 2017

@author: Parag
"""

# from fintechontwitter.fintechontwitter import DATAFRAME as df
import re

regex_strings = {
        "emoticons": r"""(?:[%s][%s]?[%s])""" % tuple(map(re.escape,
                                                          [r":;8BX=",
                                                           r"-o~'^",
                                                           r"()[]/\|DPpO"])),
        "html_tags": r'<[^>]+>',
        "user_mentions": r'(?:@[\w_]+)',
        "hashtags": r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",
        "urls": r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|\
                (?:%[0-9a-fA-F][0-9a-fA-F]))+",
        "numbers": r'(?:(?:\d+,?)+(?:\.?\d+)?)',
        "words": r"(?:[a-zA-Z0-9]+[-'_]*[a-zA-Z0-9]+)",
        "characters": r'(?:[\w])',
        "misc": r'(?:[^\w ]+)'}


tokens_re = re.compile(r'('+'|'.join([regex_strings['urls'],
                                      regex_strings['html_tags'],
                                      regex_strings['user_mentions'],
                                      regex_strings['hashtags'],
                                      regex_strings['emoticons'],
                                      regex_strings['numbers'],
                                      regex_strings['words'],
                                      regex_strings['characters'],
                                      regex_strings['misc']])+')',
                       re.VERBOSE)
regex = {key: re.compile(r'^' + pattern + '$', re.VERBOSE)
         for key, pattern in regex_strings.items()}


def preprocess(s, lowercase=False):
    tokens = tokens_re.findall(s)
    classified_tokens = {}
    if lowercase:
        tokens = [token if regex["emoticons"].search(token) else token.lower()
                  for token in tokens]
    for key in regex_strings:
        classified_tokens[key] = [token for token in tokens
                                  if regex[key].search(token)]
    return classified_tokens
