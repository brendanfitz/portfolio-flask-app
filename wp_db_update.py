import requests
import html
from os import environ
from datetime import datetime
from pymongo import MongoClient
from portfolio.utils import WordPressAPI

MONGODB_URI = environ['MONGODB_URI']


def clean_post(post):
    post = {WordPressAPI.KEY_MAPPING[k]: v
            for k, v in post.items() if k in WordPressAPI.KEY_MAPPING.keys()}
    post['title'] = html.unescape(post['title']['rendered'])
    post['date_posted']

    post['date_posted']= (datetime.strptime(post['date_posted'], '%Y-%m-%dT%H:%M:%S')
        .strftime(WordPressAPI.BLOG_DATE_FMT)
    )
    return post

def upsert_posts(posts):
    client = MongoClient(MONGODB_URI)
    db = client['portfolio']
    c = db['blogs']

    docs_updated = 0
    for post in posts:
        result = c.update_one({'wp_post_id': post['wp_post_id']},
                              {'$set': post},
                              upsert=True)
        docs_updated += result.modified_count
    client.close()

    return docs_updated

if __name__ == '__main__':
    wp = WordPressAPI()
    response = requests.get(wp.POSTS_URL, headers=wp.HEADERS, verify=True)

    posts = response.json()
    posts = [clean_post(post) for post in posts if post['status'] == 'publish']

    docs_updated = upsert_posts(posts)
    
    print(f'Upsert Complete\n{docs_updated} documents updated')
