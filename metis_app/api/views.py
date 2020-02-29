# api/views.py
from flask import render_template, request, Blueprint
from metis_app.api.nhl_game_results_scrape import nhl_scrape

api = Blueprint('api', __name__)

@api.route('/nhl_results')
def nhl_results():
    json = nhl_scrape()
    return json
