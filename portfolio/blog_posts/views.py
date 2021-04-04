from flask import render_template, abort, request, Blueprint
from portfolio.db import db
from datetime import datetime

c = db['blogs']

kwargs = dict(
    template_folder='templates/blog_posts',
    static_folder='static',
)
blog_posts = Blueprint('blog_posts', __name__, **kwargs)

@blog_posts.route('/<name>')
def blog(name):
    blog = c.find_one({'id': name})

    if blog is None:
        abort(404)

    title = blog['title']
    date = (datetime.strptime(blog['date_posted'], '%Y-%m-%d')
        .strftime('%B %d, %Y')
    )
    template = '{}.html'.format(name)
    return render_template(template, title=title, blog=True, date=date)
