# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:47:29 2020

@author: SWannell
"""

import pandas as pd
import numpy as np
import math
from scipy.stats import chi2_contingency

lbl = pd.read_csv('AmendedData\\LBL.csv')

# Format, check
lbl = lbl[['id', 'value', 'optin', 'giftaid', 'appeal', 'cell', 'warm']]
assert len(lbl['optin'].dropna()) + len(lbl['warm'].dropna()) == len(lbl)
lbl['warm'] = lbl['warm'].fillna(False).replace('OptInNotReshown', True)

# Totals
totals = lbl.groupby('cell').count()[['value']]

guardrails = {'giftaid': '', 'emailable': ''}

# Emailable donors
emailable = lbl[['optin', 'cell']].dropna().groupby('cell').sum()
emailable['warm'] = lbl[['warm', 'cell']].dropna().groupby('cell').sum()
emailable['total'] = totals['value']
emailable['count'] = emailable['optin'] + emailable['warm']
emailable.drop(columns=['optin', 'warm'], inplace=True)
# print(emailable)
guardrails['emailable'] = emailable

# Gift Aid donors
giftaid = lbl[['giftaid', 'cell']].dropna().groupby('cell').sum()
giftaid['total'] = totals['value']
giftaid.columns = ['count', 'total']
# print(giftaid)
guardrails['giftaid'] = giftaid


def ci_walters(obs,col=0,z=1.96):
    """
    obs: a 2x2 numpy array, with convs in column col
    col: an int to ID which column has conversions in
    From https://ncss-wpengine.netdna-ssl.com/wp-content/themes/ncss/pdf/\
    Procedures/PASS/Confidence_Intervals_for_the_Ratio_of_Two_Proportions.pdf
    """
    a = obs.iloc[0, col]
    b = obs.iloc[1, col]
    m, n = obs.sum(axis=1)
    p1 = a / m
    p2 = b / n
    f1 = math.log((a+0.5)/(m+0.5))
    f2 = math.log((b+0.5)/(n+0.5))
    phi = math.exp(f2-f1)  # inverted f1 and f2 as we want p2/p1 not p1/p2
    u = 1/(a+0.5)-1/(m+0.5)+1/(b+0.5)-1/(n+0.5)
    lower = phi*math.exp(-z*math.sqrt(u))
    upper = phi*math.exp(z*math.sqrt(u))
    return (lower, p2/p1, upper)


for k, metric_df in guardrails.items():
    metric_df.to_csv('AmendedData\\LBL_{}.csv'.format(k))
    [ctrl_tot, test_tot] = metric_df['total'].values
    [ctrl_conv, test_conv] = metric_df['count'].values
    ctrl_r = ctrl_conv/ctrl_tot * 100
    test_r = test_conv/test_tot * 100
    df = pd.DataFrame([[ctrl_tot - ctrl_conv, ctrl_conv],
                       [test_tot - test_conv, test_conv]],
                      columns=['non-don', 'don'], index=['ctrl', 'test'])
    exp = np.array(df.loc['ctrl'])
    obs = np.array(df.loc['test'])
    chi2, p, dof, ex = chi2_contingency(df, correction=True)
    pctChange = df['don'] / [ctrl_tot, test_tot]
    pctChange = 100*(pctChange[1] / pctChange[0] - 1)
    low_bd, relrisk, up_bd = [(a-1)*100 for a in ci_walters(df, 1)]
    print('\n====={}====='.format(k))
    print("ctrl: {:.0f}/{:.0f} = {:.1f}%".format(ctrl_conv, ctrl_tot, ctrl_r))
    print("test: {:.0f}/{:.0f} = {:.1f}%".format(test_conv, test_tot, test_r))
    print("χ²(2, N={:.0f}) = {:.2f}".format(ctrl_tot + test_tot, chi2))
    print("p = {:.2f}".format(p))
    print('Change: {:.0f}% ({:.0f} to {:.0f}%)'.format(relrisk, low_bd, up_bd))