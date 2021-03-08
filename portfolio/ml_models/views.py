# ml_models/views.py
import numpy as np
import pandas as pd
from flask import render_template, abort, request, Blueprint
from portfolio.ml_models.forms import (MoviePredictorForm, LoanPredictorForm,
                                       KickstarterPitchOutcomeForm, TitanticPredictorForm,
                                       NhlGoalsPredictorForm)
from portfolio.ml_models.db import ml_db
from statsmodels.regression.linear_model import OLSResults
import requests

ml_models = Blueprint('ml_models', __name__, template_folder="templates/ml_models")

DOMAIN_ADDR = 'http://192.168.0.162/'
DEFAULT_TIMEOUT = 1.5

def payload_from_form(form):
    payload = dict()
    for field in form:
        if field.name not in ['csrf_token', 'submit']:
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
        try:
            payload = payload_from_form(form)
            if name == 'luther':
                url = DOMAIN_ADDR + 'movie_roi' 
                response = requests.get(url, params=payload, timeout=DEFAULT_TIMEOUT)
                prediction = response.json()['prediction']
            elif name == 'mcnulty':
                url = DOMAIN_ADDR + 'lending_club_loan_default' 
                response = requests.get(url, params=payload, timeout=DEFAULT_TIMEOUT)
                prediction = response.json()['prediction']
            elif name == 'fletcher':
                url = DOMAIN_ADDR + 'kickstarter_pitch_outcome' 
                response = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
                prediction = response.json()['prediction']
            elif name == 'titantic':
                url = DOMAIN_ADDR + 'titanic'
                response = requests.get(url, params=payload, timeout=DEFAULT_TIMEOUT)
                prediction = response.json()['prediction']
            elif name == 'nhl_goals':
                url = DOMAIN_ADDR + 'nhl_player_season_scoring_total'
                response = requests.get(url, params=payload, timeout=DEFAULT_TIMEOUT)
                prediction = response.json()['prediction']
            else:
                abort(404)
        except requests.exceptions.Timeout: 
            abort(503) # service unavailable
        return render_template(template, model=True, form=form, title=title, prediction=prediction)

    return render_template(template, model=True, title=title, form=form)
