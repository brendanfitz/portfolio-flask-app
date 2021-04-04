from pymongo import MongoClient
from os import environ

MONGODB_URI = environ['MONGODB_URI']
client = MongoClient(MONGODB_URI)
db = client['portfolio']