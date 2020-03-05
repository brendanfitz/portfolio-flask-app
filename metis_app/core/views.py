# core/views.py
from flask import render_template, request, Blueprint
from metis_app.blog_posts.db import blog_db
from metis_app.visuals.db import visuals_db

core = Blueprint('core', __name__, template_folder='templates/core')

@core.route('/')
def index():
    kwargs = dict(homepage=True, blog_db=blog_db, visuals_db=visuals_db)
    return render_template('index.html', **kwargs)

@core.route('/about')
def about():
    return render_template('about.html', blog=True, title="About Me, Brendan!")
