from flask import render_template, abort, request, Blueprint
from portfolio import db
from datetime import datetime
import requests
from portfolio.utils import WordPressAPI
from portfolio import dbs

wp = WordPressAPI()

kwargs = dict(
    template_folder='templates/blog_posts',
    static_folder='static',
)
blog_posts = Blueprint('blog_posts', __name__, **kwargs)
blog_date_fmt = '%B %d, %Y'

@blog_posts.route('/<name>')
def blog(name):
    blog = dbs.blogs.find_one({'id': name})

    if blog is None:
        abort(404)

    title = blog['title']
    date = (datetime.strptime(blog['date_posted'], '%Y-%m-%d')
        .strftime(blog_date_fmt)
    )

    if blog.get('wp_post_id') is not None:
        wp_post_id = str(blog['wp_post_id'])

        wp_blog_content = blog['content']

        template = 'wp_blog_base.html'
        return render_template(template, title=title, blog=True, date=date,
                               wp_blog_content=wp_blog_content)
    else:
        template = '{}.html'.format(name)
        return render_template(template, title=title, blog=True, date=date)
