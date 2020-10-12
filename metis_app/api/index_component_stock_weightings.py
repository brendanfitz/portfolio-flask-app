# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:17:26 2020

@author: Brendan Non-Admin
"""


import requests
import json
from os import environ
import pandas as pd
import boto3

uris = ['sp500', 'dowjones']

def scrape_index_component_stocks(stock_index_name, from_s3):
    if stock_index_name not in uris:
        raise ValueError(f'stock_index_name must be in {uris}')
    
    if from_s3:
        df_scraped = df_scraped_from_s3(stock_index_name)
    else:
        df_scraped = df_scraped_from_web(stock_index_name)

    columns = ['Company', 'Weight', 'Price']
    industries = scrape_stock_industries(stock_index_name)

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

def scrape_stock_industries(stock_index_name):
    if stock_index_name == 'sp500':
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        table_num = 0
    elif stock_index_name == 'dowjones':
        url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
        table_num = 1
    else:
        raise ValueError('Index Must Be "sp500" or "dowjones"')
    df = (pd.read_html(url)[table_num]
        .assign(Symbol=lambda x: x.Symbol.str.replace('NYSE:\xa0', ''))
        .set_index('Symbol')
        .rename(columns={'GICS Sector': 'Industry'})
        .loc[:, ['Industry']]
    )
    return df


def df_scraped_from_web(stock_index_name):
    url = r'https://www.slickcharts.com/{}'.format(stock_index_name)
    response = requests.get(url)
    df = (pd.read_html(response.text)[0]
        .set_index('Symbol')
    )
    return df

def df_scraped_from_s3(stock_index_name):
    aws_config = {
        'aws_access_key_id': environ.get('METIS_APP_AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': environ.get('METIS_APP_AWS_SECRET_KEY'),
    }
    client = boto3.client('s3', **aws_config)

    response = client.get_object(
        Bucket='metis-projects',
        Key=f"stock_index_data/{stock_index_name}.json",
    )
    data = json.load(response.get('Body'))
    df = (pd.DataFrame(data['data'])
        .set_index('Symbol')
    )

    return df