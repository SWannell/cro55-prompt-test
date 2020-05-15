# -*- coding: utf-8 -*-
"""
Created on Fri May 15 16:07:28 2020

@author: SWannell
"""

import numpy as np
from scipy.stats import ttest_ind_from_stats
import matplotlib.pyplot as plt; plt.style.use('ggplot')
import seaborn as sns

np.random.seed(1234)

# Set parameters
params = {'ctrl': {'prompts': [5, 25, 50],
                   'p': [0.25, 0.375, 0.375]},
          'test': {'prompts': [15, 35, 50]}}
cellvol = 500

# Get a starting distribution that has an equal average gift
size = 10000
trial_dist = [0.48, 0.26, 0.26]
ctrl_vals = np.random.choice(params['ctrl']['prompts'], size,
                             p=params['ctrl']['p'])
test_vals = np.random.choice(params['test']['prompts'], size,
                             p=trial_dist)
print(ctrl_vals.mean(), test_vals.mean())

# set initial values in dict
params['test']['p'] = [0.48, 0.26, 0.26]
for cell in params.keys():
    params[cell]['vals'] = np.random.choice(params[cell]['prompts'],
                                            size=cellvol,
                                            p=params[cell]['p'])
    params[cell]['mean'] = params[cell]['vals'].mean()
    params[cell]['std'] = params[cell]['vals'].std()

# Plot initial dist
figs, axs = plt.subplots(2, 1, sharex=True, sharey=True)
sns.violinplot(x=params['ctrl']['vals'], color='#1d1a1c', ax=axs[0])
sns.violinplot(x=params['test']['vals'], color='#ee2a24', ax=axs[0])
alpha = 0.7
plt.setp(axs[0].collections, alpha=alpha)

# MDE calc
p_MDE = 1
t_MDE = 0
lift_MDE = 0.00
while p_MDE > 0.05:
    # Apply expected uplift - flatten the diff between prompts
    lift = np.array([-lift_MDE, 0.5*lift_MDE, 0.5*lift_MDE])
    params['test']['p'] = np.array(params['test']['p']) + lift
    for cell in params.keys():
        params[cell]['vals'] = np.random.choice(params[cell]['prompts'],
                                                size=cellvol,
                                                p=params[cell]['p'])
        params[cell]['mean'] = params[cell]['vals'].mean()
        params[cell]['std'] = params[cell]['vals'].std()
    # t-test
    t_MDE, p_MDE = ttest_ind_from_stats(
            params['ctrl']['mean'],
            params['ctrl']['std'],
            cellvol,
            params['test']['mean'],
            params['test']['std'],
            cellvol
            )
    degf = cellvol*2 - 2
    upliftMDE = lift_MDE*100
    print("Ctrl: (mean={:.2f}, std={:.2f})".format(
              params['ctrl']['mean'],
              params['ctrl']['std']),
      "\nTest: (mean={:.2f}, std={:.2f})".format(
              params['test']['mean'],
              params['test']['std']),
      "\nt({:.0f})={:.2f}, p={:.2f}, uplift={:,.0f}%\n".format(
              degf,
              t_MDE,
              p_MDE,
              upliftMDE))
    if p_MDE < 0.05:
        break
    lift_MDE += 0.01

# PLot resulting dist
sns.violinplot(x=params['ctrl']['vals'], color='#1d1a1c', ax=axs[1])
sns.violinplot(x=params['test']['vals'], color='#ee2a24', ax=axs[1])
plt.setp(axs[1].collections, alpha=alpha)