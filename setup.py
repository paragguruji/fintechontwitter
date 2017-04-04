# -*- coding: utf-8 -*-
"""
Created on Tue Apr 04 17:42:19 2017

@author: Parag
"""

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='fintechontwitter',
    version='0.0.1',
    description='Experiments to find insights from Twitter data about topic \
        "FinTech"',
    long_description=readme,
    author='Parag Guruji',
    author_email='pguruji@purdue.edu',
    url='https://github.com/paragguruji/fintechontwitter',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'data', 'log'))
)
