# api/views.py
from flask import render_template, request, Blueprint

api = Blueprint('api')

@api.route('/nhl_results')
def nhl_results():
    pass
