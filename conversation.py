import pprint

from pymongo import MongoClient
from anytree import AnyNode, RenderTree

from anytree.exporter import DotExporter
from termcolor import colored
# from graphviz import Digraph

jsonDirectory = 'C:\\Users\\mert\\Downloads\\airlines_complete\\data\\*.json'
client = MongoClient('127.0.0.1', 27017)
db = client.datachallenge
collection = db.conversation


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
        process_node = process_list.pop(0)
        children_query = collection.find({'in_reply_to_status_id': process_node.id})
        for child in children_query:
            child_node = AnyNode(id=child['id'], name=child['user']['name'], text=child['text'], parent=process_node)
            child_node.id = child['id']

            process_list.insert(0, child_node)  # put in from the stack


def conversation_length_for_userid(user_id):
    root_nodes_list = []

    print("Selecting all tweets from id: {}...".format(user_id))

    conversation_query = collection.find({'user.id': user_id, 'in_reply_to_status_id': None})  # starting from user_id
    for i, root_tweet in enumerate(conversation_query):
        root_nodes = AnyNode(id=root_tweet['id'], name=root_tweet['user']['name'], text=root_tweet['text'])
        root_nodes.id = root_tweet['id']  # Not sure if why I need to state this two times.
        # pprint.pprint("Populating: {}".format(i))
        populate_node(root_nodes)
        root_nodes_list.append(root_nodes)

    pprint.pprint('Total sum of root nodes: {}'.format(len(root_nodes_list)))
    # DotExporter(root_nodes_list[0]).to_picture("test.png")
    for i,tree in enumerate(root_nodes_list):
        if tree.height > 2:
            print("Conversation: {}".format(i))
            print(RenderTree(tree))
            print("")


print("Running script.")
conversation_length_for_userid(22536055)
