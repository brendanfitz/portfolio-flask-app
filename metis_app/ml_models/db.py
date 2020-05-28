from metis_app.ml_models.forms import (MoviePredictorForm, LoanPredictorForm,
                                       KickstarterPitchOutcomeForm, TitanticPredictorForm,
                                       NhlGoalsPredictorForm)

ml_db = [
    {
        'id': 'luther',
        'title': 'Movie ROI Prediction Model',
        'form': MoviePredictorForm,
    },
    {
        'id': 'mcnulty',
        'title': 'Lending Club Loan Default Prediction Model',
        'form': LoanPredictorForm,
    },
    {
        'id': 'fletcher',
        'title': 'Kickstarter Pitch Funding Outcome Prediction Model',
        'form': KickstarterPitchOutcomeForm,
    },
    {
        'id': 'titantic',
        'title': 'Will You Survive The Titantic?',
        'form': TitanticPredictorForm,
    },
    {
        'id': 'nhl_goals',
        'title': 'NHL Goals Scored Auotregressive Prediction Model',
        'form': NhlGoalsPredictorForm,
    },
]
