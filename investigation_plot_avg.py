# -*- coding: utf-8 -*-
"""
Created on Wed May 13 12:10:54 2020

@author: SWannell
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt; plt.style.use('ggplot')
import matplotlib.ticker as mtick

# Munge SGLBL

sglbl = pd.read_csv('RawData\\old_sglbl.csv')

for col in sglbl.columns:
    if "Date" in col:
        sglbl[col] = pd.to_datetime(sglbl[col], dayfirst=True)

sglbl.columns = ['date', 'settle_date', 'value', 'id', 'afd', 'email',
                 'privacy',
                 'giftaid', 'appeal', 'sorp', 'platform', 'status',
                 'sourcecode', 'campaign', 'source', 'medium', 'creative',
                 'audience', 'os', 'os_version', 'browser', 'browser_version',
                 'response_code', 'trans_uuid']

sglbl = sglbl.loc[:, ['date', 'value', 'id', 'medium', 'creative', 'sorp']]
sglbl['month'] = pd.DatetimeIndex(sglbl["date"]).strftime('%Y-%m')
sglbl.set_index('date', inplace=True)
sglbl.isna().sum()  # lots of NA in Medium
sglbl['medium'].fillna('Other', inplace=True)
sglbl.to_csv('AmendedData\\sglbl.csv')

# Why is email so high for UKGFR? Investigate using creative

# Make GFR and non-GFR DFs

sglbl['ukgfr'] = sglbl['sorp'].str.contains('P6269')

nonsmall = sglbl.pivot_table(values='value', index='medium',
                             aggfunc=np.count_nonzero)
nonsmall = nonsmall[nonsmall['value'] > 50].index

sg_nonsmall = sglbl[sglbl['medium'].isin(nonsmall)]
sg_nonsmall = sg_nonsmall[sg_nonsmall['value'] < 100]

ukgfr_nonsmall = sg_nonsmall[sg_nonsmall['ukgfr'] == True]
nonuk_nonsmall = sg_nonsmall[sg_nonsmall['ukgfr'] == False]

# =============================================================================
# Two-facet plot of UK GFR gift distribution, vs not
# =============================================================================

fig, axs = plt.subplots(1, 2, figsize=(14, 7), sharey=True)

plt.suptitle('2020 gift distribution by medium', fontsize=20)

sns.violinplot(x='value', y='medium', data=ukgfr_nonsmall, ax=axs[0],
               order=nonsmall)
currfmt = mtick.StrMethodFormatter('£{x:,.0f}')
axs[0].xaxis.set_major_formatter(currfmt)
axs[0].get_xaxis().set_minor_locator(mtick.AutoMinorLocator())
axs[0].grid(b=True, which='minor', color='w', axis='x', linewidth=1.0)
axs[0].set_title('UK GFR gifts')
axs[0].set_xlim((0, 100))

sns.violinplot(x='value', y='medium', data=nonuk_nonsmall, ax=axs[1],
               order=nonsmall)
axs[1].xaxis.set_major_formatter(currfmt)
axs[1].get_xaxis().set_minor_locator(mtick.AutoMinorLocator())
axs[1].grid(b=True, which='minor', color='w', axis='x', linewidth=1.0)
axs[1].set_title('Non-UK GFR gifts', fontsize=20)
axs[1].set_xlim((0, 100))
plt.savefig('Outputs\\2020_gift_values_by_channel.png')

# =============================================================================
# One facet version, 
# =============================================================================

colors = ["#1d1a1c", "#04923e"]
sns.set_palette(sns.color_palette(colors))

fig, ax = plt.subplots(1, 1, figsize=(14, 7))
sns.violinplot(x='value', y='medium', hue='ukgfr', split=True,
               data=sg_nonsmall, ax=ax, order=nonsmall, cut=0)
currfmt = mtick.StrMethodFormatter('£{x:,.0f}')
ax.xaxis.set_major_formatter(currfmt)
ax.get_xaxis().set_minor_locator(mtick.AutoMinorLocator())
ax.grid(b=True, which='minor', color='w', axis='x', linewidth=1.0)
ax.set_title('2020 gifts by medium', fontsize=20)
ax.set_xlim((0, 100))
plt.savefig('Outputs\\2020_gift_values_by_channel_split.png')