#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urllib.parse as p
import xml.etree.ElementTree as ET
import pandas as pd
import json


def get_yield_curve(year):
    url = create_url(year)

    response = requests.get(url)
    xml = response.content
    root = ET.fromstring(xml)
    
    ns = {'ns': 'http://www.w3.org/2005/Atom',
          'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata', 
          'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices'}
    
    data = list()
    for entry in root.findall('ns:entry', ns):
        content = (entry.find('ns:content', ns)
         .find('m:properties', ns)
        )
        row = dict()
        for child in content:
            row[child.tag.replace('{' + ns['d'] + '}', '')] = child.text
        data.append(row)
    
    return json.dumps(data)


def create_url(year):
    base = "https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData"
    qstr = '?$filter=year(NEW_DATE)%20eq%20{}'.format(year)
    url = base + qstr
    return url