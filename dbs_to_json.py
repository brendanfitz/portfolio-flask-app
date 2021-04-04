import json
from os import makedirs, path

DIRECTORY = 'data'

if __name__ == '__main__':
    from portfolio.blog_posts.db import blog_db
    from portfolio.visuals.db import visuals_db
    from portfolio.ml_models.db import ml_db

    dbs = {
        'blogs': blog_db,
        'visuals': visuals_db,
        'ml_models': ml_db,
    }

    makedirs(DIRECTORY, exist_ok=True)
    for db_name, db in dbs.items():
        filepath = path.join(DIRECTORY, db_name + '.json')
        with open(filepath, 'w') as f:
            json.dump(db, f, indent=2)
