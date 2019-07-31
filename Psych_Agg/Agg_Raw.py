# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 19:50:44 2019

@author: Jesus
"""

import pandas as pd
import os
pd.options.mode.chained_assignment = None




def group_unit(df, unit='leader'):

    df['name'] = df['firstname'] + " " + df['lastname']

    if unit=='leader':
        grouped = df.groupby(['name','firstname', 'lastname', 'Ccode']).sum().reset_index()

    elif unit=='year':
        grouped = df.groupby(['name','firstname', 'lastname', 'Ccode', 'year']).sum().reset_index()

    elif unit=='month':

        df.dropna(subset=['month'], inplace=True)
        df['yr_month'] = df['year'].map(str) + "-" + df['month'].map(str)
        grouped = df.groupby(['name','firstname', 'lastname', 'Ccode', 'yr_month']).sum().reset_index()

    elif unit=='quarter':

        df.dropna(subset=['month'], inplace=True)
        df['day'] = df['day'].fillna(1)
        dates = ['year', 'month', 'day']
        df[dates] = df[dates].astype(int)

        df['date'] = pd.to_datetime(df['year']*10000+df['month']*100+df['day'],format='%Y%m%d')
        df['quarter'] = df.date.dt.quarter
        df['yr_quarter'] = df['year'].map(str) + "-" + df['quarter'].map(str)
        grouped = df.groupby(['name','firstname', 'lastname', 'Ccode', 'yr_quarter']).sum().reset_index()

    return grouped


def calc_raws(df, unit='leader'):

    """
    df - rows are raw totals

    """

    df['distrust'] = df['HDIS']/(df['HDIS']+df['LDIS'])
    df['task'] = df['HTASK']/(df['HTASK']+df['LTASK'])
    df['bace'] = df['IC']/(df['IC']+df['EC'])
    df['igb'] = df['HBIAS']/(df['HBIAS']+df['LBIAS'])
    df['sc'] = df['HSC']/(df['HSC']+df['LSC'])
    df['cc'] = df['HCC']/(df['HCC']+df['LCC'])
    df['power'] = df['HPWR']/(df['HPWR']+df['LPWR'])

    df['i1'] = df.apply(i1_func, axis=1)
    df['i2'] = df.apply(i2_func, axis=1)
    df['i3'] = df.apply(i3_func, axis=1)

    df['i4a'] = df.apply(i4a_func, axis=1)
    df['i4b'] = df.apply(i4b_func, axis=1)
    df['i5ap'] = df.apply(i5ap_func, axis=1)
    df['i5pr'] = df.apply(i5pr_func, axis=1)
    df['i5re'] = df.apply(i5re_func, axis=1)
    df['i5op'] = df.apply(i5op_func, axis=1)
    df['i5th'] = df.apply(i5th_func, axis=1)
    df['i5pu'] = df.apply(i5pu_func, axis=1)

    df['p1'] = df.apply(p1_func, axis=1)
    df['p2'] = df.apply(p2_func, axis=1)
    df['p3'] = df.apply(p3_func, axis=1)
    df['p4'] = df.apply(p4_func, axis=1)
    df['p5'] = df.apply(p5_func, axis=1)

    if unit == 'leader':

        keep = ['firstname', 'lastname', 'name', 'Ccode', 'vcount', 'distrust', 'task',
                'bace', 'igb', 'sc', 'cc', 'power', 'i1', 'i2', 'i3', 'i4a', 'i4b',
                'i5ap', 'i5pr', 'i5re', 'i5op', 'i5th', 'i5pu', 'p1', 'p2', 'p3', 'p4',
                'p5']

        df = df[keep]

    elif unit == 'year':

        keep = ['firstname', 'lastname', 'name', 'year', 'Ccode', 'vcount', 'distrust', 'task',
                'bace', 'igb', 'sc', 'cc', 'power', 'i1', 'i2', 'i3', 'i4a', 'i4b',
                'i5ap', 'i5pr', 'i5re', 'i5op', 'i5th', 'i5pu', 'p1', 'p2', 'p3', 'p4',
                'p5']

        df = df[keep]

    elif unit == 'month':

        keep = ['firstname', 'lastname', 'name', 'yr_month','Ccode', 'vcount', 'distrust', 'task',
                'bace', 'igb', 'sc', 'cc', 'power', 'i1', 'i2', 'i3', 'i4a', 'i4b',
                'i5ap', 'i5pr', 'i5re', 'i5op', 'i5th', 'i5pu', 'p1', 'p2', 'p3', 'p4',
                'p5']

        df = df[keep]

        df['year'] = df['yr_month'].apply(lambda x: x.split('-')[0])
        df['month'] = df['yr_month'].apply(lambda x: x.split('-')[1])

    elif unit == 'quarter':

        keep = ['firstname', 'lastname', 'name', 'yr_quarter', 'Ccode', 'vcount', 'distrust', 'task',
                'bace', 'igb', 'sc', 'cc', 'power', 'i1', 'i2', 'i3', 'i4a', 'i4b',
                'i5ap', 'i5pr', 'i5re', 'i5op', 'i5th', 'i5pu', 'p1', 'p2', 'p3', 'p4',
                'p5']

        df = df[keep]

        df['year'] = df['yr_quarter'].apply(lambda x: x.split('-')[0])
        df['quarter'] = df['yr_quarter'].apply(lambda x: x.split('-')[1])

    return df



def convert(df):

    df.dropna(subset=['vcount', 'HDIS', 'LDIS', 'HTASK', 'LTASK', 'IC',
       'EC', 'HBIAS', 'LBIAS', 'HSC', 'LSC', 'HCC', 'LCC', 'HPWR', 'LPWR',
       'self-pun', 'self-threat', 'self oppose', 'self appeal', 'self promise',
       'self reward', 'other punish', 'other threaten', 'other oppose',
       'other appeal', 'other promise', 'other reward'], inplace=True)

    convert =['self-pun','self-threat','self oppose','self appeal','self promise','self reward','other punish',
              'other threaten','other oppose','other appeal','other promise','other reward']
    df[convert] = df[convert].astype(int)

    return df


def i1_func(x):

   try:
       l = (( (x['self appeal'] + x['self promise'] + x['self reward']) - (x['self-pun'] + x['self-threat'] + x['self oppose'])) /
        (x['self appeal'] +x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose']))

   except ZeroDivisionError:
       l = 0

   return l


def i2_func(x):

    try:
        l = ((x['self appeal'] + x['self promise']*2 + x['self reward']*3 - x['self-pun']*3 - x['self-threat']*2 - x['self oppose']) /
        ((x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose'])*3))

    except ZeroDivisionError:
        l = 0

    return l


def i3_func(x):

    try:
        l = 1 - ( ( (x['self appeal'] * x['self promise']) + (x['self appeal'] * x['self reward']) + (x['self appeal'] * x['self-pun']) +
                (x['self appeal'] * x['self-threat']) + (x['self appeal'] * x['self oppose']) + (x['self promise'] * x['self-pun']) +
                (x['self promise'] * x['self-threat']) + (x['self promise'] * x['self oppose']) + (x['self promise'] * x['self reward']) +
                (x['self reward'] * x['self-pun']) + (x['self reward'] * x['self-threat']) + (x['self reward'] * x['self oppose']) +
                (x['self-pun'] * x['self-threat']) + (x['self-pun'] * x['self oppose']) + (x['self-threat'] * x['self oppose'])

              ) /
            (15 *(((x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose'])/6) *
                  ((x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose'])/6))
            ))

    except ZeroDivisionError:
        l = 0

    return l


def i4a_func(x):

    try:
        l = 1 - abs( ( (x['self appeal'] + x['self promise'] + x['self reward']) - (x['self-pun'] + x['self-threat'] + x['self oppose'])
                     ) /
                    (x['self appeal'] +x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose'])
                   )
    except ZeroDivisionError:
        l = 0

    return l


def i4b_func(x):

    try:
        l = 1 - abs( ( (x['self appeal'] + x['self promise'] +  x['self-threat'] + x['self oppose']) - (x['self reward'] + x['self-pun'])
                      ) /
                       (x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose'])
                   )

    except ZeroDivisionError:
        l = 0

    return l



def i5ap_func(x):

    try:
        l = (x['self appeal'] / (x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose']))

    except ZeroDivisionError:
        l = 0

    return l


def i5pr_func(x):

    try:
        l = (x['self promise'] / (x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose']))

    except ZeroDivisionError:
        l = 0

    return l

def i5re_func(x):

    try:
        l = (x['self reward'] / (x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose']))

    except ZeroDivisionError:
        l = 0

    return l

def i5op_func(x):

    try:
        l = (x['self oppose'] / (x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose']))

    except ZeroDivisionError:
        l = 0

    return l

def i5th_func(x):

    try:
        l = (x['self-threat'] / (x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose']))

    except ZeroDivisionError:
        l = 0

    return l

def i5pu_func(x):

    try:
        l = (x['self-pun'] / (x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose']))

    except ZeroDivisionError:
        l = 0

    return l


def p1_func(x):

    try:
        l = (((x['other appeal'] + x['other promise'] + x['other reward']) - (x['other punish'] + x['other threaten'] + x['other oppose'])
             ) /
             (x['other appeal'] + x['other promise'] + x['other reward'] + x['other punish'] + x['other threaten'] + x['other oppose'])

            )
    except ZeroDivisionError:
        l = 0

    return l


def p2_func(x):

    try:
        l = ((x['other appeal'] + x['other promise']*2 + x['other reward']*3 - x['other punish']*3 - x['other threaten']*2 - x['other oppose']
             ) /
             ((x['other appeal'] + x['other promise'] + x['other reward'] + x['other punish'] + x['other threaten'] + x['other oppose']) *3)

            )
    except ZeroDivisionError:
        l = 0

    return l



def p3_func(x):

    try:
        l = 1 - ( ( (x['other appeal'] * x['other promise']) + (x['other appeal'] * x['other reward']) + (x['other appeal'] * x['other punish']) +
                (x['other appeal'] * x['other threaten']) + (x['other appeal'] * x['other oppose']) + (x['other promise'] * x['other punish']) +
                (x['other promise'] * x['other threaten']) + (x['other promise'] * x['other oppose']) + (x['other promise'] * x['other reward']) +
                (x['other reward'] * x['other punish']) + (x['other reward'] * x['other threaten']) + (x['other reward'] * x['other oppose']) +
                (x['other punish'] * x['other threaten']) + (x['other punish'] * x['other oppose']) + (x['other threaten'] * x['other oppose'])

              ) /
            (15 *(((x['other appeal'] + x['other promise'] + x['other reward'] + x['other punish'] + x['other threaten'] + x['other oppose'])/6) *
                  ((x['other appeal'] + x['other promise'] + x['other reward'] + x['other punish'] + x['other threaten'] + x['other oppose'])/6))
            ))

    except ZeroDivisionError:
        l = 0

    return l



def p4_func(x):

    try:
        l = ( (x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose']) /
             (x['self appeal'] + x['self promise'] + x['self reward'] + x['self-pun'] + x['self-threat'] + x['self oppose'] +
              x['other appeal'] + x['other promise'] + x['other reward'] + x['other punish'] + x['other threaten'] + x['other oppose'])
             )
    except ZeroDivisionError:
        l = 0

    return l


def p5_func(x):

    try:
        l = 1- (x['p3'] * x['p4'])

    except ZeroDivisionError:
        l = 0

    return l
