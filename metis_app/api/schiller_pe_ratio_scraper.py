# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:28:38 2020

@author: Brendan Non-Admin
"""

from pandas import read_html, to_datetime

class SchillerPERatioScraper(object):

    url = 'https://www.multpl.com/shiller-pe/table/by-year'

    def __init__(self):
        self.data = self.scrape_data()

    def scrape_data(self):
        cls = SchillerPERatioScraper
        data = (read_html(cls.url, converters={'Date': to_datetime})[0]
            .rename(columns={'Value Value': 'Schiller PE Ratio'})
            .assign(Year=lambda x: x.Date.dt.year)
            .to_dict(orient='records')
        )
        return data 