import json
import glob
import pprint

import pymongo
from anytree import AnyNode

from pymongo import MongoClient
from pymongo.errors import BulkWriteError, DuplicateKeyError

# Everything in one directory
jsonDirectory = 'C:\\Users\\Mert\\Downloads\\airlines-data\\data\\*.json'
client = MongoClient('127.0.0.1', 27017)
db = client.datachallenge
collection = db.conversation
conversations = db.conversation_trees


def create_indexes():
    print('Creating indices... ');

    collection.create_index([("id", pymongo.ASCENDING)], unique=True)
    collection.create_index([("in_reply_to_status_id", pymongo.ASCENDING)])
    collection.create_index([("in_reply_to_user_id", pymongo.ASCENDING)])
    collection.create_index([("user.id", pymongo.ASCENDING)])
    pprint.pprint(list(db.profiles.index_information()))


def process_all_json_files(directory):
    print('Scanning directory: ', jsonDirectory)
    # Finds files recursively.
    jsonFiles = glob.glob(directory)
    total = len(jsonFiles)
    fileCount = 0
    print('Found a total of: ', total)

    create_indexes()

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


def sanitize_db():
    collection.remove({"id": None})  # remove idless tweets


def find_root_tweet(tweet):
    root = tweet
    while 'in_reply_to_status_id' in root:
        # pprint.pprint(root)
        # print("{} --> {} ".format(root['id'], root['in_reply_to_status_id']))
        parent = collection.find_one({"id": root['in_reply_to_status_id']})
        if parent:
            root = parent
        else:
            # print("DEAD node for: {} which links to dead node: {}".format(root['id'], root['in_reply_to_status_id']))
            return None
    return root


def populate_node(root_node):
    process_list = [root_node]
    while process_list:
        # Remove one node at a time from the list
        process_node = process_list.pop(0)
        # Find a reply to the root node
        children_query = collection.find({'in_reply_to_status_id': process_node.id})
        for child in children_query:
            child_node = AnyNode(id=child['id'], name=child['user']['name'], text=child['text'], parent=process_node)
            child_node.id = child['id']
            process_list.insert(0, child_node)  # put on top the stack


def process_conversations():
    mention_query = collection.find({'in_reply_to_status_id': {"$ne": None}})
    for cnt, tweet in enumerate(mention_query):
        root = find_root_tweet(tweet)
        if root is not None:
            print(cnt)
            populate_node(root)


# process_all_json_files(jsonDirectory)
# sanitize_db()
create_indexes()
process_conversations()
