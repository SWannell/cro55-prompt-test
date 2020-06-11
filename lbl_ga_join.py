# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:21:45 2020

@author: SWannell
"""

import pandas as pd

start_date = '20200520'
end_date = '20200609'  # would be grab start/end dates from a log file?

# Set file paths
gaid_fp = 'AmendedData\\GADataTrans{}-{}.csv'.format(start_date, end_date)
sglbl_fp = 'AmendedData\\sglbl.csv'
# rglbl_fp = 'AmendedData\\RGLBL.csv'

# Read in data
gaid = pd.read_csv(gaid_fp)
sglbl = pd.read_csv(sglbl_fp)

# rglbl = pd.read_csv(rglbl_fp)
# for df in [trans, sglbl, rglbl]:
for df in [gaid, sglbl]:
    df.set_index('id', inplace=True)

gaid = gaid[['cell']]
print('Test IDs in GA: {}'.format(len(set(gaid.index))))

df_sg = sglbl.join(gaid)
print('IDs in SGLBL and/or GA: {}'.format(len(set(df_sg.index))))

df_sg = df_sg.dropna(subset=['cell'])
print('Test IDs in SGLBL and GA: {}'.format(len(set(df_sg.index))))

num_rgs = len(gaid[gaid.index.str.startswith('IDD')])

test_sg_ids = set(df_sg.index)
test_rg_ids = set(gaid[gaid.index.str.startswith('IDD')].index)
test_ids = test_sg_ids.union(test_rg_ids)

print('Test IDs: {}\nGA IDs: {}'.format(len(test_ids), len(gaid.index)))

mismatch_ids = test_ids.symmetric_difference(set(gaid.index))

try:
    assert len(mismatch_ids) == 0, "There are  IDs in just GA but not LBL"
except AssertionError as msg:
    print(msg)
    missing_testids = [tid for tid in gaid.index if tid not in test_ids]
    print("Missing from lbl:", missing_testids)
    missing_gaids = [tid for tid in test_ids if tid not in gaid.index]
    print("Missing from GA:", missing_gaids)

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
totals = gaid.groupby('cell').sum()
cont = totals.join(results)
cont.to_csv('AmendedData\\LBLcontingency.csv')