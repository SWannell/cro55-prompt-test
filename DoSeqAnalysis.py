# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:47:11 2020

@author: SWannell
"""

from SeqAnalysis import SeqAnalysis as seqan

# two_month_vol, cvr = 3000, 0.214
# target = int(two_month_vol * cvr)
target = 1000
ttl = 'CR055 raised prompt test_conversion %'

seq = seqan(target, ttl)  # returns the plot!!
seq.z_score
# seq.cvr_plot(ttl)
seq.crossed()
seq.summary()

#print(seq.z_score)
#print(seq.results)