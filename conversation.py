import json
import pprint

from bson import json_util
from bson.json_util import loads
from pymongo import MongoClient
from anytree import AnyNode, RenderTree

from anytree.exporter import DotExporter
from termcolor import colored
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter

# from graphviz import Digraph

jsonDirectory = 'C:\\Users\\mert\\Downloads\\airlines_complete\\data\\*.json'
client = MongoClient('127.0.0.1', 27017)
db = client.datachallenge
collection = db.conversation
collection_trees = db.conversation_trees


def process_all_conversations():
    print("Creating groups of conversations..")
    conversation_list = list(collection.aggregate([
        {"$match": {"in_reply_to_user_id": {"$ne": None}}},
        {"$group": {"_id": '$in_reply_to_user_id',
                    'count': {'$sum': 1}}}
    ]))

    print("Retrieved {} conversations.".format(len(conversation_list)))

    totalLength = 0

    for conversation in conversation_list:
        totalLength += conversation['count'] + 1  # we're counting replies so we need to add the original author as well

    pprint.pprint("Total messages in conversations: {}".format(totalLength))

    averageLength = totalLength / len(conversation_list)

    pprint.pprint("Average conversation count: {}".format(averageLength))


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


process_set = set()
root_dict = dict()


def find_root_tweet(tweet):
    root = tweet
    cache_list = [root]

    while 'in_reply_to_status_id' in root:

        parent = collection.find_one({"id": root['in_reply_to_status_id']})
        if parent:
            if parent['id'] in root_dict:  # This node is cached
                root = root_dict[parent['id']]
                break
            else:
                root = parent
                cache_list.append(root)
        else:
            break

    for cache_item in cache_list:
        root_dict[cache_item['id']] = root

    return root


def export_conversation_trees_to_db(user_id):
    root_id_list = []
    root_nodes_list = []

    print("Selecting all tweets from id: {}...".format(user_id))
    conversation_query = collection.find(
        {'user.id': user_id, 'in_reply_to_user_id': {"$ne": None}})  # Mentioning somebody
    conversation_query2 = collection.find({'in_reply_to_user_id': user_id})  # Mentioned by somebody

    print("SET A: {} B: {} ".format(conversation_query.count(), conversation_query2.count()))

    for i, tweet in enumerate(conversation_query):
        t = find_root_tweet(tweet)
        if t['id'] not in process_set:
            process_set.add(t['id'])
            root_id_list.append(t)
            if i % 1000 == 0:
                print("Processing mentions {}".format(i))

    for i, tweet in enumerate(conversation_query2):
        t = find_root_tweet(tweet)
        if t['id'] not in process_set:
            process_set.add(t['id'])
            root_id_list.append(t)
            if i % 1000 == 0:
                print("Processing mentioned {}".format(i))

    print("SET A: {} B: {} UNION: {}".format(conversation_query.count(), conversation_query2.count(), len(process_set)))

    for i, root_tweet in enumerate(root_id_list):
        root_nodes = AnyNode(id=root_tweet['id'], name=root_tweet['user']['name'], text=root_tweet['text'])
        root_nodes.id = root_tweet['id']  # Not sure if why I need to state this two times.
        if i % 1000 == 0:
            pprint.pprint("Populating: {}".format(i))
        populate_node(root_nodes)
        root_nodes_list.append(root_nodes)
    pprint.pprint('Total sum of root nodes: {}'.format(len(root_id_list)))
    # DotExporter(root_nodes_list[0]).to_picture("test.png")
    count = 0
    for i, tree in enumerate(root_nodes_list):
        count = count + len(tree.descendants) + 1
        exporter = JsonExporter(indent=2, sort_keys=True)
        json_tree = exporter.export(tree)

        collection_trees.insert_one(json.loads(json_tree))

    print("Total conversation count: {}".format(count))
    print("Average conversation length: {}".format(count / (len(root_id_list))))


def import_conversation_trees_from_db(user_id):
    documents = collection_trees.find()
    trees = []
    for i, tree in enumerate(documents):
        importer = JsonImporter()
        r1 = json_util.dumps(tree)
        root = importer.import_(r1)
        if i % 1000 == 0:
            print("Finding: {}".format(i))
        trees.append(root)
    return trees


print("Running script.")

# export_conversation_trees_to_db(22536055) # call this once if you wish to generate trees inside the DB.
trees = import_conversation_trees_from_db(22536055)

amount = 1

for i, tree in enumerate(trees[0:amount]):
    print("Conversation {}:".format(i))
    print(RenderTree(tree))
    root = tree.root

    leaves = []
    for bottom in tree.descendants:
        if bottom.is_leaf:
            leaves.append(bottom)

    print(root)
    #print(analize_sentiment(root))
    #TODO: simple textblob root and leaves and then compare!

# pprint.pprint(trees[0:3])
