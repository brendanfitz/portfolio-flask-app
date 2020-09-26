# core/views.py
from flask import render_template, abort, request, Blueprint
from metis_app.blog_posts.db import blog_db
from metis_app.visuals.db import visuals_db

blog_db.sort(reverse=True, key=lambda x: x['date_posted'])

core = Blueprint('core', __name__, template_folder='templates/core')

@core.route('/')
def index():
    blog_db_paginated = [blog_db[i:min(i+3, len(blog_db))] for i in range(0, len(blog_db), 3)]
    kwargs = dict(
        homepage=True,
        blog_db=blog_db[:6],
        visuals_db=visuals_db[:3],
        blog_db_paginated=blog_db_paginated,
    )
    return render_template('index.html', **kwargs)

@core.route('/about')
def about():
    return render_template('about.html', blog=True, title="About Me, Brendan!", date="November 27, 2020")

@core.route('/<template_name>')
def site_section_list(template_name):
    if template_name not in ['blogs_list', 'models_list', 'visuals_list',]:
         abort(404)

    kwargs = dict(homepage=True, blog_db=blog_db, visuals_db=visuals_db)
    template = '{}.html'.format(template_name)
    return render_template(template, **kwargs)
