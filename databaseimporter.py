import glob
import pprint
from subprocess import call

import pymongo
from anytree import AnyNode

from config import collection, jsonDirectory


def create_indexes():
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
        call(['C:\\Program Files\\MongoDB\\Server\\3.6\\bin\\mongoimport', '--db', 'datachallenge',
              '--collection', 'tweets', '--file', file])


def sanitize_db():
    collection.remove({"id": None})  # remove idless tweets

