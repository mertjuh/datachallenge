# Config script that contains all the settings.
from pymongo import MongoClient

jsonDirectory = 'C:\\Users\\20166300\\Downloads\\airlines_complete\\data\\*.json'  # Main folder that contains the tweets

client = MongoClient('127.0.0.1', 27017)
db = client.datachallenge
collection = db.tweets
collection_trees = db.conversation_trees

mongo_import = 'C:\\Program Files\\MongoDB\\Server\\3.6\\bin\\mongoimport'  # Mongoimport file that is found in the mongoDB bin folder.
