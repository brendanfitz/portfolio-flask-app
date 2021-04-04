# visuals/views.py
from flask import render_template, abort, request, Blueprint
from portfolio.visuals.db import visuals_db
from datetime import datetime, timedelta
from portfolio.db import db

c = db['visuals']

kwargs = dict(
    template_folder='templates/visuals',
    static_folder='static',
)
visuals = Blueprint('visuals', __name__, **kwargs)

@visuals.route('/<name>')
def visual(name):
    visual = c.find_one({'id': name})

    if visual is None:
        abort(404)

    title = visual['title']
    template = '{}.html'.format(name)
    return render_template(template, title=title, viz_page=True)
