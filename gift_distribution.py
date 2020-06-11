# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:13:37 2020

@author: SWannell
"""

import pandas as pd
import matplotlib.pyplot as plt; plt.style.use('ggplot')
import matplotlib.ticker as mtick
import seaborn as sns

lbl = pd.read_csv('AmendedData\\LBL.csv')
cells = ['ctrl', 'test']
colours = ['#1d1a1c', '#ee2a24']
lbl = lbl[['value', 'cell']]
lbl = lbl[lbl['value'] <= 100]

bins = [0, 5, 10.01, 25, 30.01, 50, 60.01, 100]

# Spine histogram - uneven bins
fig, ax = plt.subplots(1, 2, figsize=(8, 6), sharey=True)
for i, (cell, colour) in enumerate(zip(cells, colours)):
    lbl[lbl['cell'] == cell].plot.hist(color=colour, ax=ax[i],
                                     orientation="horizontal",
                                     legend=False,
                                     bins=bins)
    ax[i].set_title(cell)
    ax[i].set_xlim((0, 70))
ax[0].invert_xaxis()
ax[0].invert_yaxis()
ax[0].set_ylabel('Donation value')
plt.suptitle('CRO55 gift value by cell', fontsize=20)
currfmt = mtick.StrMethodFormatter('£{x:,.0f}')
ax[0].yaxis.set_major_formatter(currfmt)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('Outputs\\Results_SpineHist.png')
plt.show()

# Boxplot
g = sns.boxplot(x='value', y='cell', data=df, palette=colours, order=cells)
plt.title('CRO55 gift value by cell')
g.xaxis.set_major_formatter(currfmt)
plt.savefig('Outputs\\Results_Boxplot.png')