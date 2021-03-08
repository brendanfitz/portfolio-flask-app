# api/views.py
from flask import render_template, abort, request, Blueprint, send_from_directory
from flask.json import jsonify
from flask import jsonify
import datetime as dt
import os
from portfolio.api import (
    NhlGameResultsScraper,
    YieldCurveScraper,
    StockIndexDataLoader,
    SchillerPERatioScraper,
)
import json
from pandas import read_csv

ALLOWED_EXCEL_FILENAMES = [
    'S&P 500 Time Horizon Analysis.xlsx',
    'S&P 500 Visualizations.xlsx',
    'Workout_Log.xlsx',
    'Coffee.xlsx',
]
EXCEL_DIRECTORY = os.path.join('static', 'excels')

api = Blueprint('api', __name__)

@api.route('/nhl_results')
def nhl_results():
    scraper = NhlGameResultsScraper()
    return jsonify(scraper.data)

@api.route('/nhl-team-data')
def nhl_team_data():
    data = (NhlGameResultsScraper.load_team_data()
        .reset_index()
        .to_dict(orient='records')
    )
    return jsonify(data)

@api.route('/yield_curve/<year>')
def yield_curve(year):
    scraper = YieldCurveScraper(year)
    return jsonify(scraper.data)


@api.route('/excels/<filename>')
def excel_downloads(filename):
    if filename not in ALLOWED_EXCEL_FILENAMES:
        abort(404)
    return send_from_directory(EXCEL_DIRECTORY, filename, as_attachment=True)

@api.route('/index_component_stocks/<stock_index_name>')
def index_component_stocks(stock_index_name):
    try:
        scraper = StockIndexDataLoader(stock_index_name, from_s3=False)
    except ValueError:
        try:
            scraper = StockIndexDataLoader(stock_index_name, from_s3=True)
        except:
            abort(404)
    return jsonify(scraper.data)

@api.route('/schiller_pe_ratio')
def schiller_pe_ratio():
    scraper = SchillerPERatioScraper()
    return jsonify(scraper.data)
