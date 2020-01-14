# core/views.py
from flask import render_template, request, Blueprint

core = Blueprint('core', __name__, template_folder='templates/core')

@core.route('/')
def index():
    return render_template('index.html', homepage=True)

@core.route('/about')
def about():
    return render_template('about.html')
