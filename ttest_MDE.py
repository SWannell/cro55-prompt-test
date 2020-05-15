# -*- coding: utf-8 -*-
"""
Created on Fri May 15 13:45:34 2020

@author: SWannell
"""

import numpy as np
from scipy.stats import ttest_ind_from_stats

params = {'ctrl': {'prompts': [5, 25, 50],
                   'p': [0.35, 0.35, 0.3]},
          'test': {'prompts': [15, 35, 50],
                   'p': [0.35, 0.35, 0.3]}}

params['ctrl']['vol'] = 1000
ctr_drop = 0.9
params['test']['vol'] = int(params['ctrl']['vol'] * ctr_drop)

for cell in params.keys():
    params[cell]['vals'] = np.random.choice(params['ctrl']['prompts'],
                                            size=params['ctrl']['vol'],
                                            p=params['ctrl']['p'])
    params[cell]['mean'] = params[cell]['vals'].mean()
    params[cell]['std'] = params[cell]['vals'].std()

t_MDE, p_MDE = ttest_ind_from_stats(
        params['ctrl']['mean'],
        params['ctrl']['std'],
        sum(params['ctrl']['vals']),
        params['test']['mean'],
        params['test']['std'],
        sum(params['test']['vals']))

print(t_MDE, p_MDE)