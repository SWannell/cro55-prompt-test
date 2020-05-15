# -*- coding: utf-8 -*-
"""
Created on Fri May 15 13:45:34 2020

@author: SWannell
"""

import numpy as np
from scipy.stats import ttest_ind_from_stats

params = {'prompts': [5, 25, 50],
          'p': [0.35, 0.35, 0.3],
          'vol': 1000}

params['vals'] = np.random.choice(params['prompts'], size=params['vol'],
                                  p=params['p'])
params['mean'] = params['vals'].mean()
params['std'] = params['vals'].std()

p_MDE = 1
t_MDE = 0
expected_liftMDE = 1.01
while p_MDE > 0.05:
    t_MDE, p_MDE = ttest_ind_from_stats(
            params['mean'],
            params['std'],
            params['vol'],
            params['mean']*expected_liftMDE,
            params['std'],
            params['vol']
            )
    if p_MDE < 0.05:
        break
    expected_liftMDE += 0.01

print(t_MDE, p_MDE, expected_liftMDE)

degf = params['vol']*2 - 2
upliftMDE = (expected_liftMDE-1)*100

print("Ctrl: (mean={:.2f}, std={:.2f})".format(
              params['mean'],
              params['std']),
      "\nTest: (mean={:.2f}, std={:.2f})".format(
              params['mean']*expected_liftMDE,
              params['std']),
      "\nt({:.0f})={:.2f}, p={:.2f}, uplift={:,.0f}%".format(
              degf,
              t_MDE,
              p_MDE,
              upliftMDE))