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
sglbl.to_csv('AmendedData\\old_sglbl.csv')

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

fig, ax = plt.subplots(1, 1, figsize=(7, 7))
sns.violinplot(x='value', y='medium', hue='ukgfr', split=True, scale='count',
               data=sg_nonsmall, ax=ax, order=nonsmall, cut=0)
ax.xaxis.set_major_formatter(currfmt)
ax.get_xaxis().set_minor_locator(mtick.AutoMinorLocator())
ax.grid(b=True, which='minor', color='w', axis='x', linewidth=1.0)
ax.set_title('2020 gifts by medium', fontsize=20)
ax.set_xlim((0, 100))
handles, labels = fig.get_axes()[0].get_legend_handles_labels()
fig.get_axes()[0].legend([handles[0], handles[1]], ["Non UK fund", "UK fund"])
plt.savefig('Outputs\\2020_gift_values_by_channel_split.png')

# =============================================================================
# One facet version for just email
# =============================================================================

sg_email_nonsmall = sglbl[sglbl['medium'] == 'Email']
sg_email_nonsmall = sg_email_nonsmall[sg_email_nonsmall['value'] < 100]
sg_email_nonsmall = sg_email_nonsmall[sg_email_nonsmall['creative'].str.startswith('Donate', na=False)]

sg_email_creative = sg_email_nonsmall['creative'].str.split('_',
                                     expand=True).loc[:, '0':'1']
sg_email_creative.drop(0, axis=1, inplace=True)
sg_email_creative.columns = ['sendnum']
sg_email_nonsmall['sendnum'] = sg_email_creative['sendnum'].values

sendnumlist = sg_email_nonsmall['sendnum'].value_counts()
sendnumlist = sendnumlist[sendnumlist > 100]
sendnumlist = sendnumlist.index

sg_email_nonsmall = sg_email_nonsmall[sg_email_nonsmall['sendnum'].isin(sendnumlist)]

figem, axem = plt.subplots(1, 1, figsize=(14, 7))
sns.violinplot(x='value', y='sendnum', hue='ukgfr', split=True,
               data=sg_email_nonsmall, ax=axem, cut=0)
ax.xaxis.set_major_formatter(currfmt)
ax.get_xaxis().set_minor_locator(mtick.AutoMinorLocator())
ax.grid(b=True, which='minor', color='w', axis='x', linewidth=1.0)
ax.set_title('2020 gifts by send number', fontsize=20)
ax.set_xlim((0, 100))
plt.savefig('Outputs\\2020_gift_values_by_email_sendnum_split.png')

sg_email_nonsmall_ukgfr = sg_email_nonsmall[sg_email_nonsmall['ukgfr'] == True]

ukgfr_sendnums = sg_email_nonsmall_ukgfr['sendnum'].value_counts().index

fignum, axnum = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
for i, send in enumerate(ukgfr_sendnums):
    df = sg_email_nonsmall_ukgfr
    df = df[df['sendnum'] == send]
    df.plot.hist(ax=axnum[i], bins=range(0, 100, 5), color='#ee2a24')
    axnum[i].set_title(send)
plt.suptitle('Gift values for UK GFR emails', fontsize=20)
plt.savefig('Outputs\\UKGFR_gift_values_by_sendnum_split.png')

# =============================================================================
# Comparison cpc
# =============================================================================

indo_cpc_nonsmall = pd.read_csv('AmendedData\\2018-10_Indonesia_cpc_gifts.csv')

fig, ax = plt.subplots(1, 1)
sns.violinplot(x='Revenue', data=indo_cpc_nonsmall, cut=0, ax=ax)
ax.xaxis.set_major_formatter(currfmt)
ax.get_xaxis().set_minor_locator(mtick.AutoMinorLocator())
ax.grid(b=True, which='minor', color='w', axis='x', linewidth=1.0)
ax.set_title('2018-10 cpc gift values (during Indonesia)')
ax.set_xlim((0, 100))
plt.savefig('Outputs\\Indonesia_gift_values_cpc.png')

# =============================================================================
# For t-test trial
# =============================================================================

sg_nonsmall[sg_nonsmall['medium'] == 'cpc'].to_csv('AmendedData\\cpclbl.csv')

# =============================================================================
# For Rach's Q about ppc median gift
# =============================================================================

# segment = 'cpc'
# segment = 'Email'
segment = 'Social Ad'

ukgfr_segment = sglbl[(sglbl['medium']==segment) & (sglbl['ukgfr']==True)]

ukgfr_segment.describe()

figseg, axseg = plt.subplots(1, 1, figsize=(8, 5))
ukgfr_segment['value'].hist(bins=list(range(0, 100, 5)) + [100, 10000],
         color='#ee2a24', ax=axseg, edgecolor='gray', linewidth=1)
axseg.set_xlim((0, 200))
ukgfr_segment_max = ukgfr_segment['value'].max()
seg_annot = "This bin is gifts from £100-£{:,.0f}".format(ukgfr_segment_max)
axseg.annotate(seg_annot, (100, 170))
axseg.set_title('Gift values for UK GFR {}'.format(segment))
axseg.xaxis.set_major_formatter(currfmt)
seg_strip = "".join(segment.split(" "))
plt.savefig('Outputs\\ukgfr_gift_values_{}.png'.format(seg_strip))

# =============================================================================
# For information quotient for t-test
# =============================================================================

email_and_cpc = sglbl[sglbl['medium'].isin(['cpc', 'Email'])]
email_and_cpc.describe().to_csv('AmendedData\\in_target_group_describe.csv')
