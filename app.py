from db import blog_db
from flask import Flask, render_template, request, redirect
from config import Config
from forms import MoviePredictorForm
import pickle
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
import numpy as np
import pandas as pd

def my_tokenizer(doc):
    if doc.find(' / ') == -1:
        return doc.split(' ')
    else:
        return doc.split(' / ')

app = Flask(__name__)
app.config.from_object(Config)

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

@app.route('/')
def index():
    return render_template('index.html', projects=blog_db)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog/<name>')
def blog(name):
    blog_data = blog_db[name]
    title = blog_data['title']
    subtitle = blog_data['subtitle']
    template = '/blogs/{}'.format(blog_data['template'])
    return render_template(template, is_blog=True, title=title, subtitle=subtitle)

@app.route('/visuals/<name>')
def visuals(name):
    blog_data = blog_db[name]
    template = '/visuals/{}'.format(blog_data['template_visuals'])
    return render_template(template)

@app.route('/models/luther', methods=['GET', 'POST'])
def models():
    form = MoviePredictorForm()
    if request.method == 'POST':
        print(form.budget.data)
        budget_df = budget_poly_scaler.transform(budget_poly.transform([[form.budget.data]]))
        passthroughs_df = passthroughs_scaler.transform([
           [form.in_release_days.data, form.widest_release.data, form.runtime.data],
        ])
        rating_df = ohe.transform([[form.rating.data]]).toarray()
        genre_df = cv.transform([form.genre.data]).toarray()
        frames = [budget_df, passthroughs_df, rating_df, genre_df]
        row = np.concatenate(frames, axis=1)
        prediction = regr.predict(row)[0]
        return render_template('/models/02-luther.html', form=form, prediction=prediction)
    return render_template('models/02-luther.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
