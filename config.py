# Everything in one directory
from pymongo import MongoClient

jsonDirectory = 'C:\\Users\\Mert\\Downloads\\airlines-data\\data\\*.json'
client = MongoClient('127.0.0.1', 27017)
db = client.datachallenge
collection = db.tweets
collection_trees = db.conversation_trees