import os
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
from metis_app.ml_models import luther_util
from sklearn.ensemble import RandomForestClassifier
import time
import boto3
import warnings
from statsmodels.regression.linear_model import OLSResults
warnings.simplefilter("ignore", UserWarning)

LOCAL_DIRECTORY = 'metis_app/static/pickles/'
AWS_ACCESS_KEY_ID = os.environ.get('METIS_APP_AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('METIS_APP_AWS_SECRET_KEY')


if not os.path.exists(LOCAL_DIRECTORY):
    os.mkdir(LOCAL_DIRECTORY)

import sys
sys.path.append('metis_app/ml_models')

def aws_download(object_name, filename=None,
    bucket_name='metis-projects',
    bucket_directory='pickles',
    local_directory='metis_app/static/pickles'):

    if bucket_directory:
        object_path = bucket_directory + '/' + object_name
    else:
        object_path = object_name

    if filename:
        download_path =  local_directory + '/' + filename
    else:
        download_path =  local_directory + '/' + object_name

    if not os.path.isfile(download_path):
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_KEY,
        )
        s3.download_file(bucket_name, object_path, download_path)
    return download_path


class Pickle_Imports:

    def __init__(self):

        start = time.time()
        filename = 'luther_model.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.regr = pickle.load(f)
        end = time.time()
        print('Luther Model: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'budget_poly.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.budget_poly = pickle.load(f)
        end = time.time()
        print('Budget Poly: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'budget_poly_scaler.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.budget_poly_scaler = pickle.load(f)
        end = time.time()
        print('Budget Poly Scaler: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'ohe.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.ohe = pickle.load(f)
        end = time.time()
        print('OHE: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'cv.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.cv = pickle.load(f)
        end = time.time()
        print('CV: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'passthroughs_scaler.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.passthroughs_scaler = pickle.load(f)
        end = time.time()
        print('Passthroughs Scaler: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'rf.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.rf = pickle.load(f)
        end = time.time()
        print('CLF: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'kickstarter_vectorizer.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.kickstarter_vectorizer = pickle.load(f)
        end = time.time()
        print('Kickstart Vectorizer: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'kickstarter_model.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.kickstarter_model = pickle.load(f)
        end = time.time()
        print('Kickstarter Model: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'titanic_model.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.titantic_model = pickle.load(f)
        end = time.time()
        print('Titantic Model: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'nhl_goals_regression_model.pkl'
        with open(aws_download(filename), 'rb') as f:
            self.nhl_goals_model = OLSResults.load(f)
        end = time.time()
        print('NHL Goals Model: {:,.4f} seconds'.format(end - start))
