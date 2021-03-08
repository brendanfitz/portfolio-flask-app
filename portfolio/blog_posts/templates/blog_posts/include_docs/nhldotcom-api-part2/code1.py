import pandas as pd
import requests
import json
import copy
import os

url = ('https://api.nhle.com/stats/rest/en/skater/summary'
       '?isAggregate=false'
       '&isGame=false'
       '&sort=%5B%7B%22property%22:%22goals%22,%22direction%22:%22DESC%22%7D%5D'
       '&start=0'
       '&limit=100'
       '&factCayenneExp=gamesPlayed%3E=1'
       '&cayenneExp=gameTypeId=2%20and%20'
           'seasonId%3C=20192020%20and%20seasonId%3E=20192020'
      )

response = requests.get(url)
data = json.loads(response.text)
data.keys()
