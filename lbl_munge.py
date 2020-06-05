# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:30:27 2020

@author: SWannell
"""

import pandas as pd
import os

# =============================================================================
# Munge single giving data, remove PII
# =============================================================================

#fp = '{}\\sglbl.csv'
#sglbl_raw_fp = fp.format('RawData')
sglbl_raw_fp = 'RawData\\Single Giving Line By Line (7).csv'
sglbl = pd.read_csv(sglbl_raw_fp)

sglbl = sglbl[['Response_Date', 'Payment_reference', 'Response_Value',
               'Email_Opt_In',
               'Gift_Aid_Declaration', 'Appeal_Name', 'Platform',
               'Campaign_Approach_Code', 'Campaign', 'Source', 'Medium',
               'Creative', 'Audience_ad_group']]
sglbl.columns = ['date', 'id', 'value', 'optin', 'giftaid', 'appeal',
                 'platform',
                 'sourcecode', 'campaign', 'source', 'medium', 'creative',
                 'audience']
sglbl = sglbl.set_index('id')
os.remove(sglbl_raw_fp)

#sglbl_new_fp = fp.format('AmendedData')
sglbl.to_csv('AmendedData\\sglbl.csv')

# =============================================================================
# Munge regular giving data, remove PII
# =============================================================================

#rglbl_raw_fp = '{}\\RGLBL.csv'.format('RawData')
#rglbl = pd.read_csv(rglbl_raw_fp)
#rglbl = rglbl[['Payment_reference', 'RG_value', 'Email_opt_in',
#               'Gift_aid_declaration', 'Appeal_name', 'Frequency',
#               'Campaign_Approach_code', 'Campaign', 'Source', 'Medium',
#               'Creative', 'Audience_ad_group']]
#rglbl.columns = ['id', 'value', 'optin', 'giftaid', 'appeal', 'platform',
#                 'sourcecode', 'campaign', 'source', 'medium', 'creative',
#                 'audience']
#rglbl = rglbl.set_index('id')
#os.remove(rglbl_raw_fp)
#
#rglbl_new_fp = '{}\\RGLBL.csv'.format('AmendedData')
#rglbl.to_csv(rglbl_new_fp)