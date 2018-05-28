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


create_indexes()
# process_all_json_files(jsonDirectory)
sanitize_db()

# process_conversations()
