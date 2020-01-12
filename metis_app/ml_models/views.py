# ml_models/views.py
from flask import render_template, request, Blueprint
from metis_app.ml_models.forms import MoviePredictorForm, LoanPredictorForm

ml_models = Blueprint('ml_models', __name__)

@ml_models.route('/<name>', methods=['GET', 'POST'])
def ml_models(name):
    blog_data = blog_db[name]
    template = '/models/{}'.format(blog_data['template'])
    if name == 'luther':
        form = MoviePredictorForm()
    elif name == 'mcnulty':
        form = LoanPredictorForm()
    else:
        form = None
    if request.method == 'POST':
        if name == 'luther':
            budget_df = budget_poly_scaler.transform(budget_poly.transform([[form.budget.data]]))
            passthroughs_df = passthroughs_scaler.transform([
               [form.in_release_days.data, form.widest_release.data, form.runtime.data],
            ])
            rating_df = ohe.transform([[form.rating.data]]).toarray()
            genre_df = cv.transform([form.genre.data]).toarray()
            frames = [budget_df, passthroughs_df, rating_df, genre_df]
            row = np.concatenate(frames, axis=1)
            prediction = regr.predict(row)[0]
        elif name == 'mcnulty':
            print(type(form.dti.data))
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
            prediction = "{:0.1%}".format(clf.predict_proba(row)[0][1])
        return render_template(template, form=form, prediction=prediction)
    return render_template(template, form=form)
