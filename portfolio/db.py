from pymongo import MongoClient
from os import environ

class Databases:
    URI = environ['MONGODB_URI']
    COLLECTION = 'portfolio'

    def __init__(self):
        self.client = MongoClient(self.URI)
        self.db = self.client[self.COLLECTION]

        self.blogs = self.db['blogs']
        self.ml_models = self.db['ml_models']
        self.visuals = self.db['visuals']