# ml_models/views.py
import numpy as np
import pandas as pd
from flask import render_template, abort, request, Blueprint
from metis_app.ml_models.forms import MoviePredictorForm, LoanPredictorForm, KickstarterPitchOutcomeForm
from metis_app.ml_models.pickle_imports import Pickle_Imports


ml_models = Blueprint('ml_models', __name__, template_folder="templates/ml_models")

pickles = Pickle_Imports()

def luther_prediction(form):
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
    prediction = "{:0.1%}".format(pickles.clf.predict_proba(row)[0][1])
    return prediction

def fletcher_prediction(form):
    pitch = [form.pitch.data]
    pitch_vectorized = pickles.kickstarter_vectorizer.transform(pitch).toarray()
    prediction = pickles.kickstarter_model.predict(pitch_vectorized)[0]
    return prediction

@ml_models.route('/<name>', methods=['GET', 'POST'])
def models(name):
    template = '{}.html'.format(name)

    if name == 'luther':
        form = MoviePredictorForm()
        title = "Movie ROI Prediction Model"
    elif name == 'mcnulty':
        form = LoanPredictorForm()
        title = "Lending Club Loan Default Prediction Model"
    elif name == 'fletcher':
        form = KickstarterPitchOutcomeForm()
        title = "Kickstarter Pitch Funding Outcome Prediction Model"
    else:
        abort(404)

    if request.method == 'POST':
        if name == 'luther':
            prediction = luther_prediction(form)
        elif name == 'mcnulty':
            prediction = mcnulty_prediction(form)
        elif name == 'fletcher':
            prediction = fletcher_prediction(form)
        return render_template(template, model=True, form=form, title=title, prediction=prediction)

    return render_template(template, model=True, title=title, form=form)
