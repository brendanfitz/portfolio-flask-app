# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 08:34:41 2020

@author: Brendan Non-Admin
"""

import pandas as pd

fname = '.csv'
choices=[]
(pd.DataFrame(choices, columns=['value', 'label'])
    .to_csv(fname, index=False)
)
pd.read_csv(fname, index_col=0).to_records().tolist()