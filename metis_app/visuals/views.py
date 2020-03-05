# visuals/views.py
from flask import render_template, request, Blueprint
from metis_app.visuals.db import visuals_db

kwargs = dict(
    template_folder='templates/visuals',
)
visuals = Blueprint('visuals', __name__, **kwargs)

@visuals.route('/<name>')
def visual(name):
    visual_data = blog_db[name]
    title = visual_data['title']
    template = '{}.html'.format(name)
    return render_template(template, title=title, viz_page=True)
