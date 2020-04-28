# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:17:26 2020

@author: Brendan Non-Admin
"""


import requests
import pandas as pd

def scrape_sp_500_weighting_data():
    url = r'https://www.slickcharts.com/sp500'
    response = requests.get(url)

    df_scraped = pd.read_html(response.text)[0].set_index('Symbol')

    columns = ['Company', 'Weight', 'Price']
    industries = sp_500_industries()

    df = (df_scraped
             .loc[:, columns]
             .join(industries)
         )

    data = (df
        .reset_index()
        .to_dict(orient='records')
    )
    return data


def check_sector():
    mask = df.loc[:, 'GICS Sector'].isna()
    return df.loc[mask, ].empty

def sp_500_industries():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    df = (pd.read_html(url)[0]
          .set_index('Symbol')
          .loc[:, ['GICS Sector']]
         )
    return df
