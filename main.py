import calendar
import pprint
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

import conversation
import databaseimporter as importer
from analyzer import find_sentiment_for_ids
from config import jsonDirectory, collection
from conversation import RootTweetFilterOptions
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


user_ids = [56377143, 106062176, 18332190,
            22536055, 124476322, 26223583,
            2182373406, 38676903, 1542862735,
            253340062, 218730857, 45621423,
            20626359]

filter_topics = ["food", "drink", "meal", "eat", "drink", "beverage", "alcohol"]

data = find_sentiment_for_ids(user_ids[0:1], topics=filter_topics,
                              root_tweet_filter_options=RootTweetFilterOptions.AIRLINE_ONLY)

pprint.pprint(data)


def plot_data(datapoint):
    frq = datapoint['hist_freq']
    edges = datapoint['hist_edges']
    fig, ax = plt.subplots()
    ax.bar(edges[:-1], frq, width=np.diff(edges), ec="k", align="edge")
    ax.set_ylabel('Frequency')  # , fontsize=40)
    ax.set_xlabel('Sentiment')  # , fontsize=40)
    # ax.set_title('Distribution of food sentiment (unclassified entries ignored)')#, fontsize=22)

    # plt.show()
    plt.savefig("food_distribution.svg", bbox_inches='tight')
    plt.savefig("food_distribution.pdf", bbox_inches='tight')


#plot_data(data[0])

# print("Done showing.")
