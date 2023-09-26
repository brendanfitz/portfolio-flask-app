from flask import render_template, abort, request, Blueprint
from portfolio.db import db
from datetime import datetime
from os import environ
import requests
import base64
import html

wp_url = environ['WP_URL']
user = environ['WP_USER']
pw = environ['WP_PW']
creds = user + ':' + pw
token = base64.b64encode(creds.encode())
headers = {
    'Authorization': 'Basic ' + token.decode('utf-8'),
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

c = db['blogs']

kwargs = dict(
    template_folder='templates/blog_posts',
    static_folder='static',
)
blog_posts = Blueprint('blog_posts', __name__, **kwargs)
blog_date_fmt = '%B %d, %Y'

@blog_posts.route('/<name>')
def blog(name):
    blog = c.find_one({'id': name})

    if blog is None:
        abort(404)

    if blog.get('wp_post_id') is not None:
        wp_post_id = str(blog['wp_post_id'])

        response = requests.get(wp_url + wp_post_id, headers=headers, verify=True)
        data = response.json()

        title = html.unescape(data['title']['rendered'])
        wp_blog_content = html.unescape(data['content']['rendered'])
        date = (datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S')
                .strftime(blog_date_fmt)
        )

        template = 'wp_blog_base.html'
        return render_template(template, title=title, blog=True, date=date,
                               wp_blog_content=wp_blog_content)
    else:
        title = blog['title']
        date = (datetime.strptime(blog['date_posted'], '%Y-%m-%d')
            .strftime(blog_date_fmt)
        )
        template = '{}.html'.format(name)
        return render_template(template, title=title, blog=True, date=date)
