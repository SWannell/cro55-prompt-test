# -*- coding: utf-8 -*-
"""
Created on Fri May 15 13:45:34 2020

@author: SWannell
"""

import numpy as np
from scipy.stats import ttest_ind_from_stats

params = {'ctrl': {'prompts': [5, 25, 50],
                   'p': [0.35, 0.35, 0.3]},
#          'test': {'prompts': [15, 35, 50],
#                   'p': [0.35, 0.35, 0.3]}
          }

params['ctrl']['vol'] = 1000
ctr_drop = 0.9
#params['test']['vol'] = int(params['ctrl']['vol'] * ctr_drop)

for cell in params.keys():
    params[cell]['vals'] = np.random.choice(params['ctrl']['prompts'],
                                            size=params['ctrl']['vol'],
                                            p=params['ctrl']['p'])
    params[cell]['mean'] = params[cell]['vals'].mean()
    params[cell]['std'] = params[cell]['vals'].std()

p_MDE = 1
t_MDE = 0
expected_liftMDE = 1.01
while p_MDE > 0.05:
    t_MDE, p_MDE = ttest_ind_from_stats(
            params['ctrl']['mean'],
            params['ctrl']['std'],
            params['ctrl']['vol'],
            params['ctrl']['mean']*expected_liftMDE,
            params['ctrl']['std'],
            params['ctrl']['vol']
            )
    if p_MDE < 0.05:
        break
    expected_liftMDE += 0.01

print(t_MDE, p_MDE, expected_liftMDE)

degf = sum([params[cell]['vol'] for cell in params.keys()]) - 2
upliftMDE = (expected_liftMDE-1)*100

print("Ctrl: (mean={:.2f}, std={:.2f})".format(
              params['ctrl']['mean'],
              params['ctrl']['std']),
      "\nTest: (mean={:.2f}, std={:.2f})".format(
              params['ctrl']['mean']*expected_liftMDE,
              params['ctrl']['std']),
      "\nt({:.0f})={:.2f}, p={:.2f}, uplift={:,.0f}%".format(
              degf,
              t_MDE,
              p_MDE,
              upliftMDE))