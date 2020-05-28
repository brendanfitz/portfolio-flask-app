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

ml_models = Blueprint('ml_models', __name__, template_folder="templates/ml_models")

pickles = Pickle_Imports()

def luther_prediction(form):
    if (   pickles.regr is None or pickles.budget_poly is None
        or pickles.budget_poly_scaler is None or pickles.ohe is None
        or pickles.cv is None or pickles.passthroughs_scaler is None
       ):
        pickles.luther_downloads()

    budget_df = pickles.budget_poly_scaler.transform(pickles.budget_poly.transform([[form.budget.data]]))
    passthroughs_df = pickles.passthroughs_scaler.transform([
       [form.in_release_days.data, form.widest_release.data, form.runtime.data],
    ])
    rating_df = pickles.ohe.transform([[form.rating.data]]).toarray()
    genre_df = pickles.cv.transform([form.genre.data]).toarray()
    frames = [budget_df, passthroughs_df, rating_df, genre_df]
    row = np.concatenate(frames, axis=1)
    prediction = pickles.regr.predict(row)[0]
    return prediction

def mcnulty_prediction(form):
    if pickles.rf is None:
        pickles.mcnulty_downloads()

    row = pd.DataFrame({
            'loan_amnt': form.loan_amnt.data,
            'int_rate': form.int_rate.data,
            'annual_inc': form.annual_inc.data,
            'dti': form.dti.data,
            'emp_length': mu.emp_length_map[form.emp_length.data],
            'term': mu.term_map[form.term.data],
            'purpose': mu.purpose_map[form.purpose.data],
            'grade': mu.grade_map[form.grade.data],
        },
        index=[0]
    )
    prediction = "{:0.0%}".format(pickles.rf.predict_proba(row)[0, 1])
    return prediction


def titantic_prediction(form):
    if pickles.titantic_model is None:
        pickles.titantic_downloads()

    row = pd.DataFrame({
        'pclass': form.pclass.data,
        'sex': form.sex.data,
        'title': tu.title_map[form.title.data],
        'embarked': tu.embarked_map[form.embarked.data],
        'family_size': form.family_size.data,
        'is_alone': tu.is_alone(form.family_size.data),
        'age_category': tu.age_label(form.age.data),
    }, index=[0])
    prediction = pickles.titantic_model.predict(row)[0]
    if prediction:
        return "Congrats! You're a survivor like Beyonce"
    return "Oh no! It's not looking good for you. You're down like Leo."

def fletcher_prediction(form):
    if pickles.kickstarter_vectorizer is None or pickles.kickstarter_model is None:
        pickles.fletcher_downloads()

    pitch = [form.pitch.data]
    pitch_vectorized = pickles.kickstarter_vectorizer.transform(pitch).toarray()
    prediction = pickles.kickstarter_model.predict(pitch_vectorized)[0]
    return prediction

def nhl_goals_prediction(form):
    if pickles.nhl_goals_model is None:
        pickles.nhl_downloads()

    row = pd.DataFrame({
            'L1': form.l1.data,
            'L2': form.l2.data,
            'L3': form.l3.data,
            'L4': form.l4.data,
            'L5': form.l5.data,
            'season_number': form.season_number.data,
            'gamesPlayed': form.gamesPlayed.data,
            'positionCode': form.positionCode.data,
        }, index=[0]
    )
    prediction = "This player will score {:,.0f} goals".format(pickles.nhl_goals_model.predict(row)[0])
    return prediction

@ml_models.route('/<name>', methods=['GET', 'POST'])
def models(name):
    template = '{}.html'.format(name)

    if name not in [x['id'] for x in ml_db]:
        abort(404)

    model_data = next(filter(lambda x: name == x['id'], ml_db))
    form = model_data['form']()
    title = model_data['title']

    if request.method == 'POST':
        if name == 'luther':
            prediction = luther_prediction(form)
        elif name == 'mcnulty':
            prediction = mcnulty_prediction(form)
        elif name == 'fletcher':
            prediction = fletcher_prediction(form)
        elif name == 'titantic':
            prediction = titantic_prediction(form)
        elif name == 'nhl_goals':
            prediction = nhl_goals_prediction(form)
        else:
            abort(404)
        return render_template(template, model=True, form=form, title=title, prediction=prediction)

    return render_template(template, model=True, title=title, form=form)
