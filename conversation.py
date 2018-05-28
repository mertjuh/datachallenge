import json
import pprint

import pymongo
from anytree import AnyNode
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter
from bson import json_util

# from graphviz import Digraph
from config import collection_trees, collection


def create_indexes():
    print('Creating indices... ');
    collection_trees.create_index([("id", pymongo.ASCENDING)], unique=True)
    collection_trees.create_index([("user_id", pymongo.ASCENDING)])
    collection_trees.create_index([("contributors", pymongo.ASCENDING)])
    pprint.pprint(list(collection.index_information()))


def import_all_trees_to_db():
    print("Searching for all mentioning tweets...")

    node_dict = dict()
    root_nodes = dict()

    count = 0
    cursor = collection.find({"in_reply_to_status_id": {"$ne": None}},
                             {"id": 1, "in_reply_to_status_id": 1, "timestamp_ms": 1, "user.id": 1, "_id": 0}).sort(
        "timestamp_ms", pymongo.ASCENDING)

    for tweet in cursor:
        count = count + 1
        tweet_node = AnyNode(id=tweet['id'], user_id=tweet['user']['id'])
        tweet_node.id = tweet['id']
        tweet_node.parent_id = tweet['in_reply_to_status_id']
        tweet_node.user_id = tweet['user']['id']
        node_dict[tweet['id']] = tweet_node
    print("Found {} mentioning tweets, linking nodes...".format(count))

    linked_count = 0
    for key, value in node_dict.items():
        if value.parent_id in node_dict:
            value.parent = node_dict[value.parent_id]
            del value.parent_id
            # print("Linked from node_dict: {} {}".format(value, value.parent))
        elif value.parent_id in root_nodes:
            value.parent = root_nodes[value.parent_id]
            del value.parent_id
            # print("Linked from root_nodes: {} {}".format(value, value.parent))
        else:  # find the root in the database
            parent = collection.find_one({"id": value.parent_id})
            if parent is not None:
                root_node = AnyNode(id=parent['id'], user_id=parent['user']['id'])
                root_node.id = parent['id']
                root_node.user_id = parent['user']['id']
                value.parent = root_node
                del value.parent_id
                root_nodes[parent['id']] = root_node
        linked_count += 1
        if linked_count % 10000 == 0:
            print("Linked {} so far...".format(linked_count))

    print("Conversations: {}".format(len(root_nodes)))


def import_conversation_trees_from_db(user_id):
    documents = collection_trees.find({"contributors": user_id})
    trees = []
    for tree in documents:
        importer = JsonImporter()
        r1 = json_util.dumps(tree)
        root = importer.import_(r1)
        trees.append(root)
    return trees


def find_conversation_length(root_nodes):
    conversation_length = 0
    for key, value in root_nodes.items():

        contributors = []
        for msg in value.descendants:
            if msg.user_id not in contributors:
                contributors.append(msg.user_id)

        value.contributors = contributors
        exporter = JsonExporter(indent=2, sort_keys=True)
        json_tree = exporter.export(value)

        collection_trees.insert_one(json.loads(json_tree))
        conversation_length = conversation_length + len(value.descendants)

    print("conversation_length: {}".format(conversation_length))


#create_indexes()
#import_all_trees_to_db()
