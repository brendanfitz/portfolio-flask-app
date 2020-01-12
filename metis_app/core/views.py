# core/views.py
from flask import render_template, request, Blueprint

core = Blueprint('core', __name__)

@app.route('/')
def index():
    return render_template('index.html', projects=blog_db)

@app.route('/about')
def about():
    return render_template('about.html')
