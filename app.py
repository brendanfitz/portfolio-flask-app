from db import blog_db
from flask import Flask, render_template, request, redirect
from config import Config
from forms import MoviePredictorForm, LoanPredictorForm
import pickle
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
import numpy as np
import pandas as pd
import mcnulty_util

def my_tokenizer(doc):
    if doc.find(' / ') == -1:
        return doc.split(' ')
    else:
        return doc.split(' / ')

application = Flask(__name__)
application.config.from_object(Config)

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

@application.route('/')
def index():
    return render_template('index.html', projects=blog_db)

@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/blog/<name>')
def blog(name):
    blog_data = blog_db[name]
    title = blog_data['title']
    subtitle = blog_data['subtitle']
    template = '/blogs/{}'.format(blog_data['template'])
    return render_template(template, is_blog=True, title=title, subtitle=subtitle)

@application.route('/visuals/<name>')
def visuals(name):
    blog_data = blog_db[name]
    template = '/visuals/{}'.format(blog_data['template_visuals'])
    return render_template(template)

@application.route('/models/<name>', methods=['GET', 'POST'])
def models(name):
    blog_data = blog_db[name]
    template = '/models/{}'.format(blog_data['template'])
    if name == 'luther':
        form = MoviePredictorForm()
    elif name == 'mcnulty':
        form = LoanPredictorForm()
    else:
        form = None
    if request.method == 'POST':
        if name == 'luther':
            budget_df = budget_poly_scaler.transform(budget_poly.transform([[form.budget.data]]))
            passthroughs_df = passthroughs_scaler.transform([
               [form.in_release_days.data, form.widest_release.data, form.runtime.data],
            ])
            rating_df = ohe.transform([[form.rating.data]]).toarray()
            genre_df = cv.transform([form.genre.data]).toarray()
            frames = [budget_df, passthroughs_df, rating_df, genre_df]
            row = np.concatenate(frames, axis=1)
            prediction = regr.predict(row)[0]
        elif name == 'mcnulty':
            print(type(form.dti.data))
            row = pd.DataFrame({
                'dti': form.dti.data,
                'int_rate': form.int_rate.data,
                'emp_length': form.emp_length.data,
                'home_ownership': form.home_ownership.data,
                'purpose': form.purpose.data,
                'delinq_2yrs': form.delinq_2yrs.data,
                'revol_bal': form.revol_bal.data,
                'loan_amnt': form.loan_amnt.data,
                'grade': form.grade.data,
                'term': form.term.data,
                'installment': form.installment.data,
                'addr_state': form.addr_state.data,
            }, index=[0])
            prediction = "{:0.1%}".format(clf.predict_proba(row)[0][1])
        return render_template(template, form=form, prediction=prediction)
    return render_template(template, form=form)

if __name__ == '__main__':
    application.run('0.0.0.0')
