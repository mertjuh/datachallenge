import pprint

from anytree import RenderTree

import conversation
import databaseimporter as importer

from config import jsonDirectory
from conversation import find_average_conversation_length, import_conversation_trees_from_db
from sentiment_test import get_average_sentiment_for


def create_database():
    importer.create_indexes()
    importer.process_all_json_files(jsonDirectory)
    importer.sanitize_db()


def create_conversation_database():
    conversation.create_indexes()
    conversation.export_all_trees_to_db()


def print_average_conversation_lengths(user_ids):
    avg_lengths = dict()
    for user_id in user_ids:
        user_trees = import_conversation_trees_from_db(user_id)
        avg_lengths[user_id] = find_average_conversation_length(user_trees)
    pprint.pprint(avg_lengths)
    return  avg_lengths


def print_average_sentiment_scores(user_ids):
    avg_scores = dict()
    for user_id in user_ids:
        user_trees = import_conversation_trees_from_db(user_id)
        avg_scores[user_id] = get_average_sentiment_for(user_trees)
    pprint.pprint(avg_scores)
    return avg_scores


# create_database()  # run this only once!
# create_conversation_database()  # run this once too.

user_ids = [56377143, 106062176, 18332190,
            22536055, 124476322, 26223583,
            2182373406, 38676903, 1542862735,
            253340062, 218730857, 45621423,
            20626359]
# print_average_conversation_lengths(user_ids)
print_average_sentiment_scores(user_ids)

'''
print("Finding conversation length..")
conv_length = find_average_conversation_length(user_trees)
print("Average conversation length is: {}".format(conv_length))
print("Finding Sentiment score..")
get_average_sentiment_for(user_trees)  # this function gets the sentiment basically
'''
