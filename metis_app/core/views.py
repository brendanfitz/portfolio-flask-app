# core/views.py
from flask import render_template, request, Blueprint
from metis_app.blog_posts.db import blog_db

core = Blueprint('core', __name__, template_folder='templates/core')

@core.route('/')
def index():
    return render_template('index.html', homepage=True, blog_db=blog_db)

@core.route('/about')
def about():
    return render_template('about.html')
