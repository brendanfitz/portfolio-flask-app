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
    runtime = IntegerField('Runtime (minutes)', default=107)
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
    loan_amnt = FloatField('Loan Amount', default=13658)
    int_rate = FloatField('Interest Rate (%)', default=13.87)
    annual_inc = FloatField('Annual Income', default=72402)
    dti = FloatField('Debt-to-Income', default=16.7)
    emp_length = SelectField(
        'Employment Length',
        choices=choices_list('emp_length_choices.csv'),
        default='10+ years',
    )
    term = SelectField(
        'Loan Term',
        choices=[('36', '36 months'), ('60', '60 months'),],
        default='36 months',
    )
    purpose = SelectField(
        'Purpose of Loan',
        choices=choices_list('purpose_choices.csv'),
        default='Debt Consolidation',
    )
    grade = SelectField(
        'Lending Club Loan Grade',
        choices=choices_list('grade_choices.csv'),
        default='B',
    )
    submit = SubmitField("Predict")

class TitanticPredictorForm(FlaskForm):
    pclass = SelectField("Which Class Will You Be Traveling?",
        choices=[(1, "1st Class"), (2, "2nd Class"), (3, "3rd Class")],
        default="2nd Class",
    )
    sex = SelectField("Which Gender Are You?",
        choices=[('male', "Male"), ('female', "Female")],
        default="Male",
    )
    title = SelectField("What is your title?",
        choices=choices_list('title_choices.csv'),
        default="Mr"
    )
    embarked = SelectField("Where will you embark from?",
        choices=choices_list('embarked_choices.csv'),
        default="Southampton",
    )
    family_size = IntegerField("How many family members will you be traveling with?",
        default=3,
    )
    age = IntegerField("What is your age?",
        default=30,
    )
    submit = SubmitField("Find Out If You're A Survivor!")

class NhlGoalsPredictorForm(FlaskForm):
    l1 = IntegerField("Goals Last Year", default=17)
    l2 = IntegerField("Goals Two Years Ago", default=18)
    l3 = IntegerField("Goals Three Years Ago", default=18)
    l4 = IntegerField("Goals Four Years Ago", default=18)
    l5 = IntegerField("Goals Five Years Ago", default=18)
    season_number = IntegerField("How many seasons have this player been playing?", default=5)
    games_played = IntegerField("How many games will this player play this year?", default=82)
    position = SelectField("Forward or D?",
        choices=[("f", "Forward"), ("d", "D")]
    )
    submit = SubmitField("Predict!")
