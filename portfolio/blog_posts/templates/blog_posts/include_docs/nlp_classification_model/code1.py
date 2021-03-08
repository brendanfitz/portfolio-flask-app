import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

"""
Data
"""
fname = os.path.join(
    'Data',
    'kickstarter_data.json'
)
df = pd.read_json(fname, 'records')

"""
Preprocesing
"""
pat = r'(?P<pledged>.+)\npledged of (?P<goal>.+) goal\n[,\d]+\nbackers?'
df[['pledged', 'goal']] = df.goal_and_pledged_backers.str.extract(pat)

df = df.assign(
    pledged_currency=lambda x: x.pledged.str.extract('([^\d]+)'),
    pledged_amount=lambda x: x.pledged.astype(str).map(lambda x: ''.join([i for i in x if i.isdigit()])).astype(int),
    goal_currency=lambda x: x.goal.str.extract('([^\d]+)'),
    goal_amount=lambda x: x.goal.astype(str).map(lambda x: ''.join([i for i in x if i.isdigit()])).astype(int),
)
