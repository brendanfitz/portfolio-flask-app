# error_pages/handlers.py
from flask import Blueprint, render_template

error_pages = Blueprint('error_pages', __name__)

@error_pages.app_errorhandler(404)
def error_404(error):
    template_kwargs = dict(
        error_page=True,
        title="404 Error",
    )
    return render_template('error_pages/404.html', **template_kwargs), 404

@error_pages.app_errorhandler(503)
def error_503(error):
    template_kwargs = dict(
        error_page=True,
        title="503 Error",
    )
    return render_template('error_pages/503.html', **template_kwargs), 503