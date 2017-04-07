# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 04:00:28 2017

@author: Parag
"""

from fintechontwitter import DATAFRAME
from fintechontwitter.preprocess import preprocess
import pandas as pd

features = ['user_mentions', 'hashtags', 'emoticons',
            'plaintext', 'words', 'numbers', 'characters', 'rt']


def featureGen(tweet):
    feature_data = preprocess(tweet['tweet'])
    return pd.Series([feature_data[key] for key in features])

newcols = DATAFRAME.apply(featureGen, axis=1)
newcols.columns = features

df = DATAFRAME.join(newcols)
