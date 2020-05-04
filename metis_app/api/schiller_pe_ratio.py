# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:28:38 2020

@author: Brendan Non-Admin
"""

import pandas as pd

def scrape_schiller_pe_ratio_data():
    url = 'https://www.multpl.com/shiller-pe/table/by-year'
    
    df = (pd.read_html(url, converters={'Date': pd.to_datetime})[0]
          .rename(columns={'Value Value': 'Schiller PE Ratio'})
          .assign(Year=lambda x: x.Date.dt.year)
          .to_dict(orient='records')
         )
    
    return df