# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 19:44:51 2019

@author: Jesus
"""


from setuptools import setup, find_packages
import os

module_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name='Psych_Agg',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A package to aggregate data based on LTA and OPcode Raw scores',
    long_description=open(os.path.join(module_dir, 'README.md')).read(),
    install_requires=[],
    url='https://github.com/JELambert/Psych_Agg',
    author=['Joshua E. Lambert'],
    author_email=['joshua.lambert@knights.ucf.edu']
)
