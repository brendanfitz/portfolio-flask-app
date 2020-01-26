import pickle
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
import numpy as np
import pandas as pd
from metis_app.ml_models import luther_util
from metis_app.ml_models import mcnulty_util

import sys
sys.path.append('metis_app/ml_models')

class Pickle_Imports:

    def __init__(self):
        filename = 'metis_app/static/pickles/luther_model.pkl'
        with open(filename, 'rb') as f:
            self.regr = pickle.load(f)

        filename = 'metis_app/static/pickles/budget_poly.pkl'
        with open(filename, 'rb') as f:
            self.budget_poly = pickle.load(f)

        filename = 'metis_app/static/pickles/budget_poly_scaler.pkl'
        with open(filename, 'rb') as f:
            self.budget_poly_scaler = pickle.load(f)

        filename = 'metis_app/static/pickles/ohe.pkl'
        with open(filename, 'rb') as f:
            self.ohe = pickle.load(f)

        filename = 'metis_app/static/pickles/cv.pkl'
        with open(filename, 'rb') as f:
            self.cv = pickle.load(f)

        filename = 'metis_app/static/pickles/passthroughs_scaler.pkl'
        with open(filename, 'rb') as f:
            self.passthroughs_scaler = pickle.load(f)

        filename = 'metis_app/static/pickles/clf.pkl'
        with open(filename, 'rb') as f:
            self.clf = pickle.load(f)
