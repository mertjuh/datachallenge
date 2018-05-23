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
        # Remove one node at a time from the list
        process_node = process_list.pop(0)
        # Find a reply to the root node
        children_query = collection.find({'in_reply_to_status_id': process_node.id})
        for child in children_query:
            child_node = AnyNode(id=child['id'], name=child['user']['name'], text=child['text'], parent=process_node)
            child_node.id = child['id']
            process_list.insert(0, child_node)  # put on top the stack


def find_root_tweet(tweet):
    root = tweet
    # pprint.pprint(tweet)
    # pprint.pprint(tweet['in_reply_to_status_id'])

    # print("FOUND original: {}".format([root['id']]))

    while 'in_reply_to_status_id' in root:
        parent = collection.find_one({"id": root['in_reply_to_status_id']})
        if parent:
            root = parent
        else:
            break

    # pprint.pprint(root)
    # print("Root found: {}".format(root['id']))
    return root


def conversation_length_for_userid(user_id):
    root_id_list = []
    root_nodes_list = []
    process_set = set()

    print("Selecting all tweets from id: {}...".format(user_id))

    conversation_query = collection.find(
        {'user.id': user_id, 'in_reply_to_user_id': {"$ne": None}})  # Mentioning somebody

    conversation_query2 = collection.find({'in_reply_to_user_id': user_id})  # Mentioned by somebody

    print("SET A: {} B: {} ".format(conversation_query.count(), conversation_query2.count()))

    for i, tweet in enumerate(conversation_query):
        t = find_root_tweet(tweet)
        # t=tweet
        if t['id'] not in process_set:
            process_set.add(t['id'])
            root_id_list.append(t)
            if i % 1000 == 0:
                print("{}".format(i))

    for i, tweet in enumerate(conversation_query2):
        t = find_root_tweet(tweet)
        # t=tweet
        if t['id'] not in process_set:
            process_set.add(t['id'])
            root_id_list.append(t)
            if i % 1000 == 0:
                print("{}".format(i))

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
        # pprint.pprint(tree)
        # if tree.height > 2:
        #     print("Conversation: {}".format(i))
        #     print(RenderTree(tree))
        #     print("")
        count = count + len(tree.descendants) + 1
    print("Total conversation count: {}".format(count))
    print("Average conversation length: {}".format(count / (len(root_id_list))))


print("Running script.")

conversation_length_for_userid(22536055)
