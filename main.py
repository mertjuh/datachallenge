import json
import glob
from pymongo import MongoClient

jsonDirectory = 'C:\\Users\\mert\\Downloads\\airlines_complete\\airlines-1490714864176.json\\*.json'
client = MongoClient('127.0.0.1', 27017)
db = client.datachallenge
collection = db.conversation

print('Scanning directory: ', jsonDirectory)

def processAllJsonFiles(directory):
    jsonFiles = glob.glob(directory)
    print('Found a total of: ', len(jsonFiles))
    for file in jsonFiles:
        with open(file, 'r') as fp:
            for cnt, line in enumerate(fp):
                try:
                    lineJson = json.loads(line)
                    result = db.reviews.insert_one(lineJson)
                    print("Line {}: {}".format(cnt, result.inserted_id))
                except ValueError as e:
                    print("Line {} ERROR: {}", cnt, e)

processAllJsonFiles(jsonDirectory)

