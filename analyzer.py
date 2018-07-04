from config import collection
from conversation import import_conversation_trees_from_db, RootTweetFilterOptions
from sentiment_test import get_average_sentiment_for, get_sentiment_info


def find_sentiment_for_ids(id_list, topics=None, root_tweet_filter_options=RootTweetFilterOptions.BOTH,
                           include_all_data_points=True):
    '''Function that takes in all the airline_ids and processes them and returning the data using a list.'''

    print("Doing analysis for: {} using filter topic: {}".format(id_list, topics))
    list_length = len(id_list)
    return_info = []
    for index, id in enumerate(id_list, 1):
        screen_name = collection.find_one({"user.id": id})['user']['screen_name']
        print("[{}/{}] Starting analysis for: {}".format(index, list_length, screen_name))

        trees = import_conversation_trees_from_db(id, filter=topics,
                                                  root_tweet_filter_options=root_tweet_filter_options)

        sent_score = get_sentiment_info(trees, ignore_id=id)

        if include_all_data_points:
            sent_list_data = sent_score['sent_list'],
            root_sent_list_data = sent_score['root_sent_list']
        else:
            sent_list_data = None
            root_sent_list_data = None

        return_info.append({
            'id': id,
            'screen_name': screen_name,

            'filter_type': root_tweet_filter_options.name,
            # 'topics' : topics,
            'sentiment_score_mean': sent_score['mean'],
            'sentiment_score_sd': sent_score['sd'],
            'sentiment_score_min': sent_score['min'],
            'sentiment_score_max': sent_score['max'],

            'delta_negative_count': sent_score['delta_negative_count'],
            'delta_positive_count': sent_score['delta_positive_count'],
            'delta_neutral_count': sent_score['delta_neutral_count'],

            'root_negative_count': sent_score['root_negative_count'],
            'root_positive_count': sent_score['root_positive_count'],
            'root_neutral_count': sent_score['root_neutral_count'],

            'conv_average_size': sent_score['conv_average_size'],
            'conv_total_tweets': sent_score['conv_total_tweets'],
            'conv_amount': sent_score['conv_amount'],

            'response_time': sent_score['response_time'],
            'responses': sent_score['responses'],

            'hist_freq': sent_score['hist_freq'],
            'hist_edges': sent_score['hist_edges'],

            'sent_list': sent_list_data,
            'root_sent_list': root_sent_list_data

        })
    return return_info
