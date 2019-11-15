from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SelectField, SubmitField, validators
)


class MoviePredictorForm(FlaskForm):
    budget = IntegerField('Budget', default=85000000)
    in_release_days = IntegerField('In Release Days', default=273)
    widest_release = IntegerField('Widest Release', default=3674)
    runtime = IntegerField('Runtime', default=107)
    rating = SelectField(
        'Rating',
        choices=[('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R'),],
        default='pg-13',
    )
    genre = SelectField(
        'Genre',
        choices=[
            ("action", "Action"),
            ("adventure", "Adventure"),
            ("animation", "Animation"),
            ("comedy", "Comedy"),
            ("concert", "Concert"),
            ("crime", "Crime"),
            ("documentary", "Documentary"),
            ("drama", "Drama"),
            ("epic", "Epic"),
            ("family", "Family"),
            ("fantasy", "Fantasy"),
            ("historical", "Historical"),
            ("horror", "Horror"),
            ("music", "Music"),
            ("musical", "Musical"),
            ("period", "Period"),
            ("romance", "Romance"),
            ("romantic", "Romantic"),
            ("sci-fi", "Sci-Fi"),
            ("sports", "Sports"),
            ("thriller", "Thriller"),
            ("war", "War"),
            ("western", "Western"),
        ],
        default='action'
    )
    submit = SubmitField("Predict")
