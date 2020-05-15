# -*- coding: utf-8 -*-
"""
Created on Thu May 14 17:58:25 2020

@author: SWannell
"""

import numpy as np
from scipy.stats import norm, t
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

titledict = {'fontsize': 16, 'fontweight': 'bold'}

target = 1000

# =============================================================================
# Lan-DeMets spending function with OBF boundaries, t-test
# =============================================================================

q = np.linspace(0.06, 1, 30)  # 't' in literature, but reserve that for t-test
degf = target-2

alpha = 0.05
z = norm.ppf(1-alpha/2)
arg = [z/np.sqrt(el) for el in q]
f = 2-2*norm.cdf(arg)  # gives the p-value limit line
f_t = t.ppf(1-f, degf)

beta = 0.2
futil_z = norm.ppf(1-beta/2)
futil_arg = [futil_z/np.sqrt(el) for el in q]
futil_f = 2-2*norm.cdf(futil_arg)  # gives the p-value limit line
futility = t.ppf(1-futil_f, degf)*-1

figt, axt = plt.subplots(1, 1, figsize=(7, 7))
axt.plot(q, f_t, 'r-', lw=1, alpha=0.6, color='g')  # success
axt.plot(q, -f_t, 'r-', lw=1, alpha=0.6, color='r')  # failure
axt.plot(q, futility, 'r-', lw=1, alpha=0.6, color='k')  # futility
axt.fill_between(q, f_t, max(f_t)*np.ones(len(f_t)), color='g', alpha=0.5)
axt.fill_between(q, -f_t, min(-f_t)*np.ones(len(f_t)), color='r', alpha=0.5)
axt.fill_between(q, futility, -f_t, alpha=0.3, color='k')

# =============================================================================
# Use data
# =============================================================================

cpc = pd.read_csv('AmendedData\\cpclbl.csv')  # Test data
cpc['date'] = pd.to_datetime(cpc['date'], yearfirst=True)
cpc = cpc.set_index('date')
cpc_uk = cpc[cpc['ukgfr'] == True]
cpc_nt = cpc[cpc['ukgfr'] == False]

ctrl = cpc_nt['value'].resample('W').count()
test = cpc_uk['value'].resample('2D').count()

res = {'ctrl': {}, 'test': {}}
res['ctrl']['lbl'] = cpc_nt
res['test']['lbl'] = cpc_uk
res['ctrl']['counts'] = ctrl
res['test']['counts'] = test

for cell in res.keys():
    date_agg = res[cell]['counts'].index
    cumu = pd.DataFrame(index=date_agg,
                        columns=['n', 'var', 'mean'])
    for dt in date_agg:
        cumu.loc[dt, 'n'] = res[cell]['counts'].loc[:dt].sum()
        strdt = dt.strftime('%Y-%m-%d')
        cumu.loc[dt, 'var'] = res[cell]['lbl']['value'].loc[:strdt].var(ddof=1)
        cumu.loc[dt, 'mean'] = res[cell]['lbl']['value'].loc[:strdt].mean()
    cumu.reset_index(drop=True, inplace=True)
    res[cell]['cumu'] = cumu

# trim the whole thing, else it's too long for the plot
for cell in res.keys():
    res[cell]['cumu'] = res[cell]['cumu'].loc[:7]

# Want a data frame with columns n, t, q
t_score = pd.DataFrame(index=res['ctrl']['cumu'].index,
                       columns=['n', 't', 'q'])

t_score['n'] = res['ctrl']['cumu']['n'] + res['test']['cumu']['n']

# t-Statistic Allowing Unequal Variance (Welch)
t_num = res['test']['cumu']['mean'] - res['ctrl']['cumu']['mean']
t_denom1 = res['test']['cumu']['var']/res['test']['cumu']['n']
t_denom2 = res['ctrl']['cumu']['var']/res['ctrl']['cumu']['n']
t_denom = (t_denom1+t_denom2) ** 0.5
t_score['t'] = t_num / t_denom

t_score['q'] = 1 / (t_denom1 + t_denom2)

# plot against boundaries
axt.plot(t_score['q'], t_score['t'], color='#000000')
plt.title('CRO55 prompt test', fontsize=16)
plt.xlabel('% recruited')
plt.ylabel('t-score')
axt.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
test_descrip = "Lan-DeMets spending function, O’Brien-Fleming type boundaries"
figt.text(0, -0.05, test_descrip, color='gray', fontsize=10)
ldm_fp = 'Outputs\\Results_Target' + str(target) + '.png'
axt.set_ylim((-8, 8))
axt.set_xlim((0, 1))
plt.savefig(ldm_fp)
plt.show()

# =============================================================================
# Success check
# =============================================================================

current_q = t_score.iloc[-1]['q']
current_df = t_score.iloc[-1]['n'] - 2
current_t = t_score.iloc[-1]['t']

current_z = norm.ppf(1-alpha/2)
current_arg = current_z/np.sqrt(current_q)
current_p = 2-2*norm.cdf(current_arg)
current_t_bdr = t.ppf(1-current_p, current_df)

current_z_futil = norm.ppf(1-beta/2)
current_arg_futil = current_z_futil/np.sqrt(current_q)
current_p_futil = 2-2*norm.cdf(current_arg_futil)
current_t_bdr_futil = t.ppf(1-current_p_futil, current_df)

# Has it crossed the t-boundary?
print("Current t:", "%.2f" % current_t,
      "\nCurrent bdry:", "%.2f" % current_t_bdr)
if abs(current_t) > current_t_bdr:
    print("STOP: t crossed outer boundary - stop test, reject null")
elif current_t < current_t_bdr_futil:
    print("STOP: t crossed futility boundary - stop test, but don't reject H0")
else:
    print("t between boundaries - continue test")