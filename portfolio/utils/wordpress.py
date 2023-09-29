from os import environ
import base64

class WordPressAPI:
    KEY_MAPPING = {
        'id': 'wp_post_id', 
        'slug': 'id', 
        'title': 'title', 
        'date': 'date_posted', 
        'modified': 'date_modified'
    }
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    POSTS_URL = environ['WP_URL']
    BLOG_DATE_FMT = '%Y-%m-%d'

    def __init__(self):
        user = environ['WP_USER']
        pw = environ['WP_PW']
        creds = user + ':' + pw
        token = base64.b64encode(creds.encode())
        self.HEADERS['Authorization'] = 'Basic ' + token.decode('utf-8')