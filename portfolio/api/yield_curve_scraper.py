#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse as p
import xml.etree.ElementTree as ET
import pandas as pd


class YieldCurveScraper(object):
    # There is an error most likely caused by some xml changes per the below link
    # https://home.treasury.gov/developer-notice-xml-changes
    tmap = {
        'Id': 'ID',
        'NEW_DATE': 'Date',
        'BC_1MONTH': '1 Month',
        'BC_2MONTH': '2 Month',
        'BC_3MONTH': '3 Month',
        'BC_4MONTH': '4 Month',
        'BC_6MONTH': '6 Month',
        'BC_1YEAR': '1 Year',
        'BC_2YEAR': '2 Year',
        'BC_3YEAR': '3 Year',
        'BC_5YEAR': '5 Year',
        'BC_7YEAR': '7 Year',
        'BC_10YEAR': '10 Year',
        'BC_20YEAR': '20 Year',
        'BC_30YEAR': '30 Year',
    }

    def __init__(self, month):
        self.month= month
        self.url = self.create_url()
        self.data = self.get_yield_curve()
    
    def create_url(self):
        base = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml'
        qstr = f'?data=daily_treasury_yield_curve&field_tdr_date_value_month={self.month}'
        url = base + qstr
        return url
    
    def get_yield_curve(self):
        response = requests.get(self.url)
        xml = response.content
        root = ET.fromstring(xml)
    
        ns = {'ns': 'http://www.w3.org/2005/Atom',
              'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata',
              'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices'}
    
        self.data = list()
        for entry in root.findall('ns:entry', ns):
            content = (entry.find('ns:content', ns)
             .find('m:properties', ns)
            )
            row = dict()
            for child in content:
                treasury_name = self.treasury_map(child.tag, ns['d'])
                if treasury_name != 'BC_30YEARDISPLAY':
                    percent_yield = child.text
                    row[treasury_name] = percent_yield
            self.data.append(row)
    
        return self.data

    @staticmethod
    def treasury_map(scraped_name, ns):
        clean_name = scraped_name.replace('{' + ns + '}', '')
        return YieldCurveScraper.tmap.get(clean_name, clean_name)