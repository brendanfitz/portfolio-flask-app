# ml_models/views.py
import numpy as np
import pandas as pd
from flask import render_template, abort, request, Blueprint
from metis_app.ml_models.forms import (MoviePredictorForm, LoanPredictorForm,
                                       KickstarterPitchOutcomeForm, TitanticPredictorForm,
                                       NhlGoalsPredictorForm)
from metis_app.ml_models.pickle_imports import Pickle_Imports
from metis_app.ml_models import mcnulty_util as mu
from metis_app.ml_models import titanic_util as tu
from metis_app.ml_models.db import ml_db
from statsmodels.regression.linear_model import OLSResults
import requests

ml_models = Blueprint('ml_models', __name__, template_folder="templates/ml_models")

def payload_from_form(form):
    payload = dict()
    for field in form:
        if field.name != 'csrf_token':
            payload[field.name] = field.data
    return payload

@ml_models.route('/<name>', methods=['GET', 'POST'])
def models(name):
    template = '{}.html'.format(name)

    if name not in [x['id'] for x in ml_db]:
        abort(404)

    model_data = next(filter(lambda x: name == x['id'], ml_db))
    form = model_data['form']()
    title = model_data['title']

    if request.method == 'POST':
        payload = payload_from_form(form)
        if name == 'luther':
            url ='http://192.168.0.162/movie_roi' 
            response = requests.get(url, params=payload)
            prediction = response.json()['prediction']
        elif name == 'mcnulty':
            prediction = None
        elif name == 'fletcher':
            prediction = None
        elif name == 'titantic':
            prediction = None
        elif name == 'nhl_goals':
            prediction = None
        else:
            abort(404)
        return render_template(template, model=True, form=form, title=title, prediction=prediction)

    return render_template(template, model=True, title=title, form=form)
