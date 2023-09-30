# core/views.py
from flask import render_template, abort, request, Blueprint
from portfolio import dbs

core = Blueprint('core', __name__, template_folder='templates/core')

@core.route('/')
def index():
    kwargs = dict(
        homepage=True,
        blog_db=list(dbs.blogs.find({}, {'id': 1, 'title': 1}).sort("date_posted", -1).limit(6)),
        visuals_db=list(dbs.visuals.find({}, {'id': 1, 'title': 1}).sort("date_posted", -1).limit(6)),
        ml_db=list(dbs.ml_models.find({}, {'id': 1, 'title': 1}).sort("date_posted", -1).limit(6)),
        title="Homepage",
    )
    return render_template('index.html', **kwargs)

@core.route('/about')
def about():
    return render_template('about.html', blog=True, title="About Me, Brendan!", date="November 27, 2020")

@core.route('/<template_name>')
def site_section_list(template_name):
    if template_name not in ['blogs_list', 'models_list', 'visuals_list',]:
         abort(404)

    if template_name == 'blogs_list':
        c = dbs.blogs
    elif template_name == 'models_list':
        c = dbs.ml_models
    else:
        c = dbs.visuals

    kwargs = dict(
        homepage=True,
        posts=list(c.find({}, {'id': 1, 'title': 1}).sort("date_posted", -1)),
        title=template_name.replace('_', ' ').title()
    )
    template = '{}.html'.format(template_name)
    return render_template(template, **kwargs)
