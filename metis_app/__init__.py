# metis_app/__init__.py
from flask import Flask
from metis_app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from metis_app.core.views import core
from metis_app.blog_posts.views import blog_posts
#from metis_app.ml_models.views import ml_models
from metis_app.visuals.views import visuals

app.register_blueprint(core)
app.register_blueprint(blog_posts, url_prefix='/blogs')
#app.register_blueprint(ml_models, url_prefix='/ml_models')
#app.register_blueprint(visuals, url_prefix='visuals')
