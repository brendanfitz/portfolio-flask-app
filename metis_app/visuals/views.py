# visuals/views.py
from flask import render_template, request, Blueprint
from metis_app.visuals.db import blog_db

kwargs = dict(
    template_folder='templates/visuals',
)
visuals = Blueprint('visuals', __name__, **kwargs)

@visuals.route('/<name>')
def visual(name):
    template = blog_db[name]
    return render_template(template, viz_page=True)
