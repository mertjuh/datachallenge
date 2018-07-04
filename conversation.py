import json
import pprint
from enum import Enum

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


def export_all_trees_to_db():
    print("Searching for all mentioning tweets...")

    node_dict = dict()
    root_nodes = dict()

    count = 0
    # find all mentioning tweets, sorted by time
    cursor = collection.find({"in_reply_to_status_id": {"$ne": None}},
                             {"id": 1, "in_reply_to_status_id": 1, "timestamp_ms": 1, "user.id": 1, "_id": 0}).sort(
        "timestamp_ms", pymongo.ASCENDING)

    # create a node for a tweet
    for tweet in cursor:
        count = count + 1
        tweet_node = AnyNode(id=tweet['id'], user_id=tweet['user']['id'])
        tweet_node.id = tweet['id']
        tweet_node.parent_id = tweet['in_reply_to_status_id']
        tweet_node.user_id = tweet['user']['id']
        node_dict[tweet['id']] = tweet_node
    print("Found {} mentioning tweets, linking nodes...".format(count))

    linked_count = 0

    # look for the parent node, if it exists, add the tweet as the child node and so on.
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
    conversation_length = 0

    # also store the contributors inside the tree for performance reasons since we don't have to traverse trees when looking for a certain ID
    for key, value in root_nodes.items():

        contributors = []
        for msg in value.descendants:
            if msg.user_id not in contributors:
                contributors.append(msg.user_id)

        value.contributors = contributors
        exporter = JsonExporter(indent=2, sort_keys=True)
        json_tree = exporter.export(value)  # serialize the tree and store it

        collection_trees.insert_one(json.loads(json_tree))
        conversation_length = conversation_length + len(value.descendants)

    print("conversation_length: {}".format(conversation_length))


class RootTweetFilterOptions(Enum):  # filter whether we wish to include certain conversation starters
    AIRLINE_ONLY = 1
    NO_AIRLINE = 2
    BOTH = 3


def import_conversation_trees_from_db(user_id, filter=None, root_tweet_filter_options=RootTweetFilterOptions.BOTH):
    '''Main function that retrieves conversations inside the database.'''
    documents = collection_trees.find({"contributors": user_id})

    print("Found: {} documents.".format(documents.count()))

    trees = []
    for tree in documents:

        root_tweet = collection.find_one({"id": tree['id']})

        if (root_tweet_filter_options == RootTweetFilterOptions.AIRLINE_ONLY and root_tweet['user']['id'] != user_id) \
                or (
                root_tweet_filter_options == RootTweetFilterOptions.NO_AIRLINE and root_tweet['user']['id'] == user_id):
            continue

        if filter is not None:
            root_tweet_text = root_tweet['text'].lower()
            if not any(f in root_tweet_text for f in filter):  # topic is not inside tweet, skip it
                continue

        importer = JsonImporter()
        r1 = json_util.dumps(tree)
        root = importer.import_(r1)
        trees.append(root)
    return trees


def find_average_conversation_length(trees):
    trees_count = len(trees)
    conversation_count = 0
    for tree in trees:
        conversation_count = conversation_count + len(tree.descendants) + 1
    return conversation_count / trees_count
