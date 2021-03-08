# core/views.py
from flask import render_template, abort, request, Blueprint
from portfolio.blog_posts.db import blog_db
from portfolio.visuals.db import visuals_db
from portfolio.ml_models.db import ml_db

blog_db.sort(reverse=True, key=lambda x: x['date_posted'])

core = Blueprint('core', __name__, template_folder='templates/core')

@core.route('/')
def index():
    kwargs = dict(
        homepage=True,
        blog_db=blog_db[:6],
        visuals_db=visuals_db[:6],
        ml_db=ml_db[:6],
    )
    return render_template('index.html', **kwargs)

@core.route('/about')
def about():
    return render_template('about.html', blog=True, title="About Me, Brendan!", date="November 27, 2020")

@core.route('/<template_name>')
def site_section_list(template_name):
    if template_name not in ['blogs_list', 'models_list', 'visuals_list',]:
         abort(404)

    kwargs = dict(
        homepage=True,
        blog_db=blog_db,
        visuals_db=visuals_db,
        ml_db=ml_db,
    )
    template = '{}.html'.format(template_name)
    return render_template(template, **kwargs)
