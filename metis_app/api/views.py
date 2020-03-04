# api/views.py
from flask import render_template, request, Blueprint
from metis_app.api.nhl_game_results_scrape import nhl_scrape
from flask import jsonify
import datetime as dt
import os
from metis_app.api.yield_curve import get_yield_curve

api = Blueprint('api', __name__)

@api.route('/nhl_results')
def nhl_results():
    basedir = os.path.join('metis_app', 'api', 'static', 'api', 'data')
    season_end = dt.date(2020, 4, 4)

    if dt.date.today() > season_end:
        filename = os.path.join(basedir, f"nhl_results_{season_end}.json")
        with open(season_end, 'r') as f:
            json = f.read()
    else:
        today = dt.datetime.today().strftime('%Y%m%d')
        filename = os.path.join(basedir, f"nhl_results_{today}.json")

        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                json = f.read()
        else:
            if not os.path.isdir(basedir):
                os.makedirs(basedir)

            json = nhl_scrape()

            with open(filename, 'w') as f:
                f.write(json)

    return json

@api.route('yield_curve/<year>')
def yield_curve(year):
    json = get_yield_curve(year)
    return json
