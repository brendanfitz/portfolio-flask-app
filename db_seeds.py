import json
from os.path import join 
from pymongo import MongoClient
from dbs_to_json import DIRECTORY
from os import environ

db_names = [
    'blogs',
    'visuals',
    'ml_models',
]
MONGODB_URI = environ['MONGODB_URI']


if __name__ == '__main__':
    dbs = dict()
    for db_name in db_names:
        filepath = join(DIRECTORY, db_name + '.json')
        with open(filepath) as f:
            dbs[db_name] = json.load(f)
    
    client = MongoClient(MONGODB_URI)
    
    db = client['portfolio']
    
    for db_name, db_data in dbs.items():
        c = db[db_name]
    
        c.delete_many({})
        
        c.insert_many(db_data)
        
    client.close()
