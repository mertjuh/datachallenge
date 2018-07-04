import glob
import pprint
from subprocess import call

import pymongo

from config import collection, jsonDirectory, mongo_import


def create_indexes():
    # Creating indexes first, then adding the data

    print('Creating indices... ');

    collection.create_index([("id", pymongo.ASCENDING)], unique=True)
    collection.create_index([("in_reply_to_status_id", pymongo.ASCENDING)])
    collection.create_index([("in_reply_to_user_id", pymongo.ASCENDING)])
    collection.create_index([("user.id", pymongo.ASCENDING)])
    collection.create_index([("text", pymongo.ASCENDING)])
    collection.create_index([("timestamp_ms", pymongo.ASCENDING)])
    pprint.pprint(list(collection.index_information()))


def process_all_json_files(directory):
    print('Scanning directory: ', jsonDirectory)
    # Finds files recursively.
    jsonFiles = glob.glob(directory)
    total = len(jsonFiles)
    fileCount = 0
    print('Found a total of: ', total)

    create_indexes()

    for i, file in enumerate(jsonFiles):
        print("Processing: {} {}".format(i, file))
        call([mongo_import, '--db', 'datachallenge',
              '--collection', 'tweets', '--file', file])


def sanitize_db():
    # remove tweets that do not contain an ID since they are corrupted.

    collection.remove({"id": None})  # remove idless tweets
