import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
from sklearn.naive_bayes import GaussianNB
from metis_app.ml_models import luther_util
from metis_app.ml_models import mcnulty_util
import time


import sys
sys.path.append('metis_app/ml_models')

class Pickle_Imports:

    def __init__(self):

        start = time.time()
        filename = 'metis_app/static/pickles/luther_model.pkl'
        with open(filename, 'rb') as f:
            self.regr = pickle.load(f)
        end = time.time()
        print('Luther Model: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'metis_app/static/pickles/budget_poly.pkl'
        with open(filename, 'rb') as f:
            self.budget_poly = pickle.load(f)
        end = time.time()
        print('Budget Poly: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'metis_app/static/pickles/budget_poly_scaler.pkl'
        with open(filename, 'rb') as f:
            self.budget_poly_scaler = pickle.load(f)
        end = time.time()
        print('Budget Poly Scaler: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'metis_app/static/pickles/ohe.pkl'
        with open(filename, 'rb') as f:
            self.ohe = pickle.load(f)
        end = time.time()
        print('OHE: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'metis_app/static/pickles/cv.pkl'
        with open(filename, 'rb') as f:
            self.cv = pickle.load(f)
        end = time.time()
        print('CV: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'metis_app/static/pickles/passthroughs_scaler.pkl'
        with open(filename, 'rb') as f:
            self.passthroughs_scaler = pickle.load(f)
        end = time.time()
        print('Passthroughs Scaler: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'metis_app/static/pickles/clf.pkl'
        with open(filename, 'rb') as f:
            self.clf = pickle.load(f)
        end = time.time()
        print('CLF: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'metis_app/static/pickles/kickstarter_vectorizer.pkl'
        with open(filename, 'rb') as f:
            self.kickstarter_vectorizer = pickle.load(f)
        end = time.time()
        print('Kickstart Vectorizer: {:,.4f} seconds'.format(end - start))

        start = time.time()
        filename = 'metis_app/static/pickles/kickstarter_model.pkl'
        with open(filename, 'rb') as f:
            self.kickstarter_model = pickle.load(f)
        end = time.time()
        print('Kickstarter Model: {:,.4f} seconds'.format(end - start))
