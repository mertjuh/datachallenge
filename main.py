import json
import glob
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

jsonDirectory = 'C:\\Users\\mert\\Downloads\\airlines_complete\\data\\*.json'
client = MongoClient('127.0.0.1', 27017)
db = client.datachallenge
collection = db.conversation

print('Scanning directory: ', jsonDirectory)


def process_all_json_files(directory):
    jsonFiles = glob.glob(directory)
    total = len(jsonFiles)
    fileCount = 0
    print('Found a total of: ', total)



    for file in jsonFiles:
        with open(file, 'r') as fp:
            jsonlist = []
            fileCount += 1
            print('[{}/{}]Processing: {}'.format(fileCount, total, file))
            for cnt, line in enumerate(fp):
                try:
                    lineJson = json.loads(line)
                    jsonlist.append(lineJson)
                    # result = collection.insert_one(lineJson)

                    # print("Line {}: {}".format(cnt, result.inserted_id))
                except ValueError as e:
                    print("Line {} ERROR: {}".format(cnt, e))
            try:
                result = collection.insert_many(jsonlist)
                print('Inserted {} out of {} documents.'.format(result.inserted_ids.__len__(), len(jsonlist)))
            except BulkWriteError as e:
                print("BulkwriteError: {}".format(e.details))


process_all_json_files(jsonDirectory)
