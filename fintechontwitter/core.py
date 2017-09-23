# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 04:00:28 2017

@author: Parag
"""

from collections import Counter
from itertools import chain
from fintechontwitter.preprocess import load_frame
from matplotlib import pyplot
import pandas as pd
import logging
import mpld3

logger = logging.getLogger('fintechontwitter')

df = load_frame()
#logger.info("building counters.....")
#user_mentions_counter = Counter(chain(*df.user_mentions))
#hashtags_counter = Counter(chain(*df.hashtags))
#emoticons_counter = Counter(chain(*df.emoticons))


def date_aspect(d, a):
    if a == 'date':
        return d.date()
    if a == 'hour':
        return d.hour
    if a == 'dayofweek':
        return d.dayofweek


def tweets_by_time_dimention(dframe, dim, label="tweet_count"):
    r = dframe.groupby(dframe['date'].map(
            lambda x: date_aspect(x, dim))).count()[[0]]
    r.index.name = dim
    return r.rename(columns={r.columns[0]: label})


def row_query(dframe, query):
    if not query:
        return dframe
    if not isinstance(query, list):
        query = [query]
    criteria = None
    for q in query:
        condition = q.get('condition', None)
        val = q.get('value', None)
        column_name = q.get('column_name', None)
        if column_name not in dframe.columns:
            continue
        if condition is None:
            condition = lambda x: val in x
        if criteria is None:
            criteria = dframe[column_name].map(condition)
        else:
            criteria = criteria & dframe[column_name].map(condition)
    return dframe[criteria]


def generate_trend_plot(tags, entity_type, time_aspect):
    if not isinstance(tags, list):
        tags = [tags]
    plotframe = None
    for tag in tags:
        eligible_tweets = row_query(df,
                                    {'column_name': entity_type,
                                     'value': tag})
        plot_col = tweets_by_time_dimention(eligible_tweets, time_aspect, tag)
        if plotframe is None:
            plotframe = plot_col
        else:
            plotframe = pd.concat([plotframe, plot_col], axis=1)
    pyplot.title("Trend Analysis of " + entity_type + " by " + time_aspect)
    pyplot.xlabel(time_aspect)
    pyplot.ylabel("tweet count")
    pyplot.plot(plotframe)
    pyplot.legend(plotframe.columns.values, loc='best', title=entity_type)
    pyplot.xticks(rotation=45)
    pyplot.grid(linestyle='dotted', alpha=0.5)
    mpld3.show_d3()
#    ret = mpld3.fig_to_dict(pyplot.gcf())
#    pyplot.gcf().clear()
#    return ret

#
#top5 = user_mentions_counter.most_common(5)
#plotframe = None
#
#for i in top5:
#    tag = i[0]
#    eligible_tweets = row_query(df,
#                                {'column_name': 'user_mentions',
#                                 'value': tag})
#    plot_col = tweets_by_time_dimention(eligible_tweets, 'dayofweek', tag)
#    if plotframe is None:
#        plotframe = plot_col
#    else:
#        plotframe = pd.concat([plotframe, plot_col], axis=1)
#
## plotframe.plot.line(use_index=True, title="Daily Trend of Top 5 User Mentions")
#
#
#pyplot.title("Trend Analysis of Top Users")
#pyplot.xlabel('hour')
#pyplot.ylabel("tweet count")
## pyplot.xlim(pyplot.xlim()[0], pyplot.xlim()[1] + 0)
#pyplot.plot(plotframe)
#pyplot.legend(plotframe.columns.values, loc='best', title='Users')
#pyplot.xticks(rotation=45)
#pyplot.grid(linestyle='dotted', alpha=0.5)
## pyplot.gcf().autofmt_xdate()
#mpld3.show()
## pyplot.gcf().clear()
