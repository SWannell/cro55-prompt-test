# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:58:44 2020

@author: SWannell
"""

import pandas as pd

fp = 'RawData\\Analytics Master View Transactions 20181001-20181031.csv'
df = pd.read_csv(fp, skiprows=6)
df.dropna(inplace=True)
df['Revenue'] = df['Revenue'].str.replace('£', '')
df['Revenue'] = pd.to_numeric(df['Revenue'])
df = df[~df['Transaction ID'].str.startswith('IDD')]
df.drop(['Tax', 'Shipping', 'Quantity'], axis=1, inplace=True)

df.to_csv('AmendedData\\2018-10_Indonesia_cpc_gifts.csv')