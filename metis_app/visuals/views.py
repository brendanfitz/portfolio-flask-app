# visuals/views.py
from flask import render_template, abort, request, Blueprint
from metis_app.visuals.db import visuals_db
from datetime import datetime, timedelta

kwargs = dict(
    template_folder='templates/visuals',
    static_folder='static',
)
visuals = Blueprint('visuals', __name__, **kwargs)

@visuals.route('/<name>')
def visual(name):
    if name not in visuals_db.keys():
        abort(404)

    visual_data = visuals_db[name]
    title = visual_data['title']
    template = '{}.html'.format(name)
    return render_template(template, title=title, viz_page=True)
