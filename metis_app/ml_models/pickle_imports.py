import pickle
import pickle
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
import numpy as np
import pandas as pd
from metis_app.models import mcnulty_util

filename = 'templates/models/pickles/luther_model.pkl'
with open(filename, 'rb') as f:
    regr = pickle.load(f)

filename = 'templates/models/pickles/budget_poly.pkl'
with open(filename, 'rb') as f:
    budget_poly = pickle.load(f)

filename = 'templates/models/pickles/budget_poly_scaler.pkl'
with open(filename, 'rb') as f:
    budget_poly_scaler = pickle.load(f)

filename = 'templates/models/pickles/ohe.pkl'
with open(filename, 'rb') as f:
    ohe = pickle.load(f)

filename = 'templates/models/pickles/cv.pkl'
with open(filename, 'rb') as f:
    cv = pickle.load(f)

filename = 'templates/models/pickles/passthroughs_scaler.pkl'
with open(filename, 'rb') as f:
    passthroughs_scaler = pickle.load(f)

filename = 'templates/models/pickles/clf.pkl'
with open(filename, 'rb') as f:
    clf = pickle.load(f)
