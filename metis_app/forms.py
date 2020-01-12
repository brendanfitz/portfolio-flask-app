from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SelectField, FloatField, SubmitField, validators
)


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

class LoanPredictorForm(FlaskForm):
    dti = FloatField('Debt-to-Interest', default=16.7)
    int_rate = FloatField('Interest Rate (%)', default=13.8)
    emp_length = SelectField(
        'Employment Length',
        choices=[
            ('< 1 year', '< 1 year'),
            ('1 year', '1 year'),
            ('2 years', '2 years'),
            ('3 years', '3 years'),
            ('4 years', '4 years'),
            ('5 years', '5 years'),
            ('6 years', '6 years'),
            ('7 years', '7 years'),
            ('8 years', '8 years'),
            ('9 years', '9 years'),
            ('10+ years', '10+ years'),
            ('Not provided', 'Not provided'),
        ],
        default='10+ years',
    )
    home_ownership = SelectField(
        'Home Ownership Status',
        choices=[
            ('MORTGAGE', 'Mortage'),
            ('OWN', 'Own'),
            ('RENT', 'Rent'),
            ('OTHER', 'Other'),
            ('NONE', 'None'),
        ],
        default='Mortgage',
    )
    purpose = SelectField(
        'Purpose of Loan',
        choices=[
            ('car', 'Car'),
            ('credit_card', 'Credit Card'),
            ('debt_consolidation', 'Debt Consolidation'),
            ('educational', 'Educational'),
            ('home_improvement', 'Home Improvement'),
            ('house', 'House'),
            ('major_purchase', 'Major Purchase'),
            ('medical', 'Medical'),
            ('moving', 'Moving'),
            ('renewable_energy', 'Renewable Energy'),
            ('small_business', 'Small Business'),
            ('vacation', 'Vacation'),
            ('wedding', 'Wedding'),
            ('other', 'Other'),
        ],
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
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
            ('E', 'E'),
            ('F', 'F'),
            ('G', 'G'),
        ],
        default='B',
    )
    term = SelectField(
        'Loan Term',
        choices=[
            ('36 months', '36 months'),
            ('60 months', '60 months'),
        ],
        default='36 months',
    )
    installment = FloatField('Installment', default=420)
    addr_state = SelectField(
        'State',
        choices=[
            ('AK', 'AK'),
            ('AL', 'AL'),
            ('AR', 'AR'),
            ('AZ', 'AZ'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DC', 'DC'),
            ('DE', 'DE'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('IA', 'IA'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('MA', 'MA'),
            ('MD', 'MD'),
            ('ME', 'ME'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MO', 'MO'),
            ('MS', 'MS'),
            ('MT', 'MT'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('NE', 'NE'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NV', 'NV'),
            ('NY', 'NY'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VA', 'VA'),
            ('VT', 'VT'),
            ('WA', 'WA'),
            ('WI', 'WI'),
            ('WV', 'WV'),
            ('WY', 'WY'),
        ],
        default='CA',
    )
    submit = SubmitField("Predict")
