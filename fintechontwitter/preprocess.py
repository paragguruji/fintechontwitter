# -*- coding: utf-8 -*-
"""
Created on Wed Apr 05 17:53:34 2017

@author: Parag
"""

# from fintechontwitter.fintechontwitter import DATAFRAME as df
import re
from collections import Counter

key_sequence = ['urls', 'html_tags', 'user_mentions', 'hashtags', 'emoticons',
                'numbers', 'words', 'characters', 'misc']

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
                                     ['numbers', 'hashtags',
                                      'words', 'characters']]) +
                          r')')
regex = {key: re.compile(r'^' + pattern + '$', re.VERBOSE)
         for key, pattern in regex_strings.items()}


def preprocess(s):
    s = s.replace('\N', ' ').replace('\n', ' ').strip()
    while('  ' in s):
        s = s.replace('  ', ' ')
    tokens = tokens_re.findall(s)
    plaintext = s
    classified_tokens = {}
    for key in key_sequence:
        classified_tokens[key] = [token for token in tokens
                                  if regex[key].search(token)]
        if key not in ['words', 'numbers', 'hashtags', 'characters', 'misc']:
            plaintext = re.sub(regex_strings[key], "", plaintext)
    classified_tokens['plaintext'] = \
        ' '.join(plaintext_re.findall(plaintext)).replace('#', '')
    classified_tokens['rt'] = s.startswith('RT')
    classified_tokens['words'] = Counter(classified_tokens['words'])
    return classified_tokens
