import calendar
import pprint
from datetime import datetime

import conversation
import databaseimporter as importer
from analyzer import find_sentiment_for_ids
from config import jsonDirectory, collection
from conversation import find_average_conversation_length, import_conversation_trees_from_db
from sentiment_test import get_average_sentiment_for

import matplotlib.pyplot as plt


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
    return avg_lengths


def print_average_sentiment_scores(user_ids):
    avg_scores = dict()
    for user_id in user_ids:
        user_trees = import_conversation_trees_from_db(user_id)
        avg_scores[user_id] = get_average_sentiment_for(user_trees)
    pprint.pprint(avg_scores)
    return avg_scores


def sort_conversation_trees_by_day(trees):
    hours_dict = dict()
    return_hours_dict = dict()

    for hour in range(0, 7):
        hours_dict[calendar.day_name[hour]] = []

    for tree in trees:
        document = collection.find_one({"id": tree.root.id})
        text = document['text']
        timestamp = document['timestamp_ms']
        created_at = document['created_at']

        dat = datetime.fromtimestamp(int(timestamp) / 1000)
        day = calendar.day_name[dat.weekday()]
        hours_dict[day].append(tree)

    for key, value in hours_dict.items():
        # return_hours_dict[key] = find_average_conversation_length(value)
        return_hours_dict[key] = get_average_sentiment_for(value)

    return return_hours_dict


def sort_conversation_trees_by_hour(trees):
    hours_dict = dict()
    return_hours_dict = dict()

    for hour in range(0, 24):
        hours_dict[hour] = []

    for tree in trees:
        document = collection.find_one({"id": tree.root.id})
        text = document['text']
        timestamp = document['timestamp_ms']
        created_at = document['created_at']

        dat = datetime.fromtimestamp(int(timestamp) / 1000)
        time = (dat.hour - 2) % 24
        hours_dict[time].append(tree)

    for key, value in hours_dict.items():
        # return_hours_dict[key] = find_average_conversation_length(value)
        return_hours_dict[key] = get_average_sentiment_for(value)

    return return_hours_dict


# create_database()  # run this only once!
# create_conversation_database()  # run this once too.
# nltk.download('vader_lexicon') # run this once too.


'''user_ids = [56377143, 106062176, 18332190,
            22536055, 124476322, 26223583,
            2182373406, 38676903, 1542862735,
            253340062, 218730857, 45621423,
            20626359]
            
print_average_sentiment_scores(user_ids)

filter = ["netherlands", "holland", "europe"]
trees = import_conversation_trees_from_db(22536055,
                                          filter=filter)  # american air: 22536055)
print("Finished searching, finding sentiment...")
sent_score = get_average_sentiment_for(trees)
sent_score_with_filtered_id = get_average_sentiment_for(trees, ignore_id=22536055)

print("Final sentiment score is {} for the following filter: {}".format(sent_score, filter))
print("Final sentiment score after filtering id: {} is {} for the following filter: {}".format(22536055,
                                                                                               sent_score_with_filtered_id,
                                                                                               filter))
'''

# START FROM HERE:

user_ids = [56377143, 106062176, 18332190,
            22536055, 124476322, 26223583,
            2182373406, 38676903, 1542862735,
            253340062, 218730857, 45621423,
            20626359]

filter_topics = ["food", "drink", "meal", "eat", "drink", "beverage", "alcohol"]
data = find_sentiment_for_ids(user_ids[1:2], topics=filter_topics)  # [12:13] is last

pprint.pprint(data)
