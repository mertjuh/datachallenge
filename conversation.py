import pprint

from pymongo import MongoClient

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


def process_conversations_for(user_id):
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


process_conversations_for(22536055)
