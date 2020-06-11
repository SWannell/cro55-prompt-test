# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 14:51:09 2020

@author: SWannell
"""

import pandas as pd

lbl = pd.read_csv('AmendedData\\LBL.csv')
lbl = lbl[lbl['value'] <= 100]

em = pd.read_csv('AmendedData\\LBL_emailable.csv', index_col=0)
em_pct = em['count'] / em['total']

modest = 12.44
hopeful = 30

projected = pd.DataFrame(index=['ctrl', 'test'],
                         columns=['upfront', 'modest', 'hopeful'])

projected['upfront'] = lbl.groupby('cell').sum()['value']
projected['modest'] = projected['upfront'] + (em['count'] * modest)
projected['hopeful'] = projected['upfront'] + (em['count'] * hopeful)

projected.to_csv('AmendedData\\IncomeProjections.csv')