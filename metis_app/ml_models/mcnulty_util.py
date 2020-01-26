import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.pipeline import FeatureUnion, Pipeline

class ItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict.loc[:, self.key]

def poly_pipeline(features, degree):
    poly_steps = [('selector', ItemSelector(key=features)),
                  ('poly', PolynomialFeatures(degree=degree, include_bias=False))]
    pipeline = Pipeline(poly_steps)
    return pipeline

def dummy_pipeline(feature_name):
    feature = [feature_name]
    steps = [('selector', ItemSelector(key=feature)),
             ('enc', OneHotEncoder())]
    pipeline = Pipeline(steps)
    return pipeline

def feature_transformer_list(features, degree):
    transformer_list = list()
    numerics = [x for x in features if independents[x] == 'numeric']
    if numerics:
        numeric_trans = ('numeric', poly_pipeline(numerics, degree))
        transformer_list.append(numeric_trans)
    dummy_vars = [x for x in features if independents[x] == 'dummy']
    if dummy_vars:
        dummy_steps = list()
        for dummy in dummy_vars:
            step = ('{}_enc'.format(dummy), dummy_pipeline(dummy))
            dummy_steps.append(step)
        transformer_list += dummy_steps
    return transformer_list

def clf_pipeline(clf, features, degree):
    transformer_list = feature_transformer_list(features, degree)
    return Pipeline([('union', FeatureUnion(transformer_list=transformer_list)),
                     ('clf', clf)])
