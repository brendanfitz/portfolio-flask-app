from flask import render_template, request, Blueprint
from metis_app.blog_posts.db import blog_db
from datetime import datetime

kwargs = dict(
    template_folder='templates/blog_posts',
    static_folder='static',
)
blog_posts = Blueprint('blog_posts', __name__, **kwargs)

@blog_posts.route('/<name>')
def blog(name):
    blog_data = blog_db[name]
    title = blog_data['title']
    date = (datetime.strptime(blog_data['date_posted'], '%Y-%m-%d')
        .strftime('%B %d, %Y')
    )
    template = '{}.html'.format(name)
    return render_template(template, title=title, blog=True, date=date)
