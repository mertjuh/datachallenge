from config import collection
from conversation import import_conversation_trees_from_db
from sentiment_test import get_average_sentiment_for, get_sentiment_info


def find_sentiment_for_ids(id_list, topics=None):
    print("Doing analysis for: {} using filter topic: {}".format(id_list, topics))
    list_length = len(id_list)
    return_info = []
    for index, id in enumerate(id_list, 1):
        screen_name = collection.find_one({"user.id": id})['user']['screen_name']
        print("[{}/{}] Starting analysis for: {}".format(index, list_length, screen_name))

        trees = import_conversation_trees_from_db(id, filter=topics)

        sent_score = get_sentiment_info(trees, ignore_id=id)

        return_info.append({
            'id': id,
            'screen_name': screen_name,
            #  'average_conv_length':
            'topics': topics,
            'sentiment_score_mean': sent_score['mean'],
            'sentiment_score_sd': sent_score['sd'],
            'sentiment_score_min': sent_score['min'],
            'sentiment_score_max': sent_score['max'],

            'negative_count': sent_score['negative_count'],
            'positive_count': sent_score['positive_count'],
            'neutral_count': sent_score['neutral_count'],

            'conv_average_size': sent_score['conv_average_size'],
            'conv_total_tweets': sent_score['conv_average_size'],
            'conv_amount': sent_score['conv_average_size'],

            'response_time': sent_score['response_time'],
        })
    return return_info
