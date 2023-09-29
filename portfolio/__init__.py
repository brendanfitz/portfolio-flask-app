# portfolio/__init__.py
from flask import Flask
from portfolio.config import Config
from os import environ
from portfolio.db import Databases

dbs = Databases()

app = Flask(__name__)
app.config.from_object(Config)

from portfolio.core.views import core
from portfolio.blog_posts.views import blog_posts
from portfolio.ml_models.views import ml_models
from portfolio.visuals.views import visuals
from portfolio.api.views import api
from portfolio.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(blog_posts, url_prefix='/blogs')
app.register_blueprint(ml_models, url_prefix='/ml_models')
app.register_blueprint(visuals, url_prefix='/visuals')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(error_pages)

@app.context_processor
def inject_gid():
    return dict(
        gtm_ga4_id=environ.get('GA4_MEASUREMENT_ID'),
        gtm_ua_id=environ.get('UA_TRACKING_ID'),
        gtm_id=environ.get('GTM_ID'),
    )