from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SelectField, FloatField, SubmitField,
    TextAreaField, validators
)
import os
import pandas as pd

def choices_list(filename):
    filepath = os.path.join(
        'metis_app',
        'ml_models',
        'static',
        filename,
    )
    return (pd.read_csv(filepath, index_col=0)
        .to_records()
        .tolist()
    )

class KickstarterPitchOutcomeForm(FlaskForm):
    pitch = TextAreaField('Pitch')
    submit = SubmitField("Predict")

class MoviePredictorForm(FlaskForm):
    budget = IntegerField('Budget', default=85000000)
    in_release_days = IntegerField('In Release Days', default=273)
    widest_release = IntegerField('Widest Release', default=3674)
    runtime = IntegerField('Runtime', default=107)
    rating = SelectField(
        'Rating',
        choices=[('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R'),],
        default='PG-13',
    )
    genre = SelectField(
        'Genre',
        choices=choices_list('genre_choices.csv'),
        default='action',
    )
    submit = SubmitField("Predict")

class LoanPredictorForm(FlaskForm):
    dti = FloatField('Debt-to-Interest', default=16.7)
    int_rate = FloatField('Interest Rate (%)', default=13.8)
    emp_length = SelectField(
        'Employment Length',
        choices=choices_list('emp_length_choices.csv'),
        default='10+ years',
    )
    home_ownership = SelectField(
        'Home Ownership Status',
        choices=choices_list('home_ownership_choices.csv'),
        default='Mortgage',
    )
    purpose = SelectField(
        'Purpose of Loan',
        choices=choices_list('purpose_choices.csv'),
        default='Debt Consolidation',
    )
    delinq_2yrs = SelectField(
        'Has the borrow had any delinquencies in the past 2 years?',
        choices=[(x, x) for x in range(30)],
        default=0,
    )
    revol_bal = FloatField('Revolving Balance', default=15000)
    loan_amnt = FloatField('Loan Amount', default=13658)
    grade = SelectField(
        'Lending Club Loan Grade',
        choices=choices_list('grade_choices.csv'),
        default='B',
    )
    term = SelectField(
        'Loan Term',
        choices=[('36 months', '36 months'), ('60 months', '60 months'),],
        default='36 months',
    )
    installment = FloatField('Installment', default=420)
    addr_state = SelectField(
        'State',
        choices=choices_list('addr_state_choices.csv'),
        default='CA',
    )
    submit = SubmitField("Predict")
