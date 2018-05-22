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


def conversation_length_for_userid(
        user_id):  # TODO: this is not finished, lacking conversations where user_id doesn't start.
    process_list = []
    print("Selecting all tweets from id: {}...".format(user_id))
    count = 0
    conversation_query = collection.find({'user.id': user_id, 'in_reply_to_status_id': None})  # starting from user_id
    for user_id_tweet in conversation_query:
        count = count + 1
        # pprint.pprint('Initializing tweet: {}'.format(count))
        process_list.append(user_id_tweet['id'])

    pprint.pprint(conversation_query.count())

    tweet_sum = 0
    while process_list:
        conversation_tweet_id = process_list.pop(0)  # remove first item that needs to be processed.
        tweet_sum = tweet_sum + 1
        # print("Total tweets: {}".format(tweet_sum))
        for conversation_child_tweet in collection.find({'in_reply_to_status_id': conversation_tweet_id}):
            process_list.append(conversation_child_tweet['id'])

    pprint.pprint('Total sum of tweets: {}'.format(tweet_sum))
    conversation_length = tweet_sum / count
    pprint.pprint('Conversation length: {}'.format(conversation_length))


print("Running script.")
conversation_length_for_userid(22536055)
