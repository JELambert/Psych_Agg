#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 09:34:33 2021

@author: joshualambert
"""

import pandas as pd
import os

os.chdir('..')
def main():
    l = pd.read_csv('../data/csv/lead_lta.csv')