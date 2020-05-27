# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:21:45 2020

@author: SWannell
"""

import pandas as pd

start_date = '20200520'
end_date = '20200526'  # would be grab start/end dates from a log file?

# Set file paths
trans_fp = 'AmendedData\\GADataTrans{}-{}.csv'.format(start_date, end_date)
sglbl_fp = 'AmendedData\\sglbl.csv'
# rglbl_fp = 'AmendedData\\RGLBL.csv'

# Read in data
trans = pd.read_csv(trans_fp)
sglbl = pd.read_csv(sglbl_fp)
# rglbl = pd.read_csv(rglbl_fp)
# for df in [trans, sglbl, rglbl]:
for df in [trans, sglbl]:
    df.set_index('id', inplace=True)
trans = trans[['cell']]

print('Transactions in test: {}'.format(len(trans)))

df_sg = sglbl.join(trans)
print('Transactions in SGLBL: {}'.format(len(df_sg)))
df_sg = df_sg.dropna(subset=['cell'])
print('Transactions in SGLBL and test: {}'.format(len(df_sg)))

num_rgs = len(trans[trans.index.str.startswith('IDD')])

assert len(df_sg) + num_rgs == len(trans)

# RG merge
#df_rg = rglbl.join(trans)
#print('Transactions in RGLBL: {}'.format(len(df_rg)))
#df_rg = df_rg.dropna(subset=['cell'])
#print('Transactions in RGLBL and test: {}'.format(len(df_rg)))

# Final LBL
# lbl = df_sg.append(df_rg)
lbl = df_sg
lbl.to_csv('AmendedData\\LBL.csv')

#sglbl['warm'] = sglbl['warm'].fillna(False).replace('OptInNotReshown', True)

# Contingency
df = lbl[['optin', 'giftaid', 'cell']]
results = df.groupby('cell').sum()
totals = trans.groupby('cell').sum()
cont = totals.join(results)
cont.to_csv('AmendedData\\LBLcontingency.csv')
