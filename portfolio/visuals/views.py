# visuals/views.py
from flask import render_template, abort, request, Blueprint
from portfolio.visuals.db import visuals_db
from datetime import datetime, timedelta

kwargs = dict(
    template_folder='templates/visuals',
    static_folder='static',
)
visuals = Blueprint('visuals', __name__, **kwargs)

@visuals.route('/<name>')
def visual(name):
    if name not in [x['id'] for x in visuals_db]:
        abort(404)

    visual_data = next(filter(lambda x: name == x['id'], visuals_db))
    title = visual_data['title']
    template = '{}.html'.format(name)
    return render_template(template, title=title, viz_page=True)
