# visuals/views.py
from flask import render_template, request, Blueprint
from metis_app.visuals.db import blog_db

visuals = Blueprint('visuals', __name__)

@visuals.route('/visuals/<name>')
def visuals(name):
    blog_data = blog_db[name]
    template = '/visuals/{}'.format(blog_data['template_visuals']) # MUST UPDATE THIS
    return render_template(template)
