import json
import glob
import pymongo

from pymongo import MongoClient
from pymongo.errors import BulkWriteError, DuplicateKeyError

# Everything in one directory
jsonDirectory = 'C:\\Users\\mert\\Downloads\\airlines_complete\\data\\*.json'
client = MongoClient('127.0.0.1', 27017)
db = client.datachallenge
collection = db.conversation

# Index incomplete. Makes querying faster and decreases running time.
print('Creating index for field \'id\'. ')
collection.create_index([("id", pymongo.ASCENDING)], unique=True)

print('Scanning directory: ', jsonDirectory)


def process_all_json_files(directory):
    # Finds files recursively.
    jsonFiles = glob.glob(directory)
    total = len(jsonFiles)
    fileCount = 0
    print('Found a total of: ', total)

    for file in jsonFiles:
        # Opening every file.
        with open(file, 'r') as fp:
            duplicatecount = 0
            jsonlist = []
            fileCount += 1
            print('[{}/{}]Processing: {}'.format(fileCount, total, file))
            for cnt, line in enumerate(fp):
                try:
                    # One line equals one tweet and its attributes.
                    lineJson = json.loads(line)
                    # jsonlist.append(lineJson)
                    result = collection.insert_one(lineJson)

                    # print("Line {}: {}".format(cnt, result.inserted_id))
                except ValueError as e:
                    print("Line {} ERROR: {}".format(cnt, e))
                except DuplicateKeyError as dke:
                    duplicatecount += 1
            if duplicatecount > 0:
                print('Skipped {} amount of duplicate data.'.format(duplicatecount))
                # try:
                #    result = collection.insert_many(jsonlist)
                #    print('Inserted {} out of {} documents.'.format(result.inserted_ids.__len__(), len(jsonlist)))
                # except BulkWriteError as e:
                #    print("BulkwriteError: {}".format(e.details))


process_all_json_files(jsonDirectory)
