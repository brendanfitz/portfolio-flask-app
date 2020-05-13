# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:17:26 2020

@author: Brendan Non-Admin
"""


import requests
import pandas as pd

uris = {'SP500': 'sp500', 'DowJones': 'dowjones'}

def scrape_index_component_stocks(index):
    url = r'https://www.slickcharts.com/{}'.format(uris[index])
    response = requests.get(url)

    df_scraped = pd.read_html(response.text)[0].set_index('Symbol')

    columns = ['Company', 'Weight', 'Price']
    industries = stock_industries(index)

    df_without_weights = (df_scraped
             .loc[:, columns]
             .join(industries)
             .sort_values(['Industry', 'Weight'], ascending=[True, False])
         )

    industry_weights = (df_without_weights
        .groupby(['Industry'], as_index=False)['Weight'].sum()
        .set_index('Industry')
        .rename(columns={'Weight': 'Industry Weight'})
    )

    df = (df_without_weights
        .join(industry_weights, on=['Industry'])
        .fillna("Unknown")
        .sort_values(['Industry Weight', 'Weight'], ascending=[False, False])
    )

    data = (df
        .reset_index()
        .to_dict(orient='records')
    )
    return data

def all_stocks_have_industries(df):
    mask = df.loc[:, 'Industry'].isna()
    return df.loc[mask, ].empty

def stock_industries(index):
    if index == 'SP500':
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        table_num = 0
    elif index == 'DowJones':
        url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
        table_num = 1
    else:
        raise ValueError('Index Must Be "SP500" or "DowJones"')
    df = (pd.read_html(url)[table_num]
        .assign(Symbol=lambda x: x.Symbol.str.replace('NYSE:\xa0', ''))
        .set_index('Symbol')
        .rename(columns={'GICS Sector': 'Industry'})
        .loc[:, ['Industry']]
     )
    return df
