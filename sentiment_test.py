import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer

from config import collection
from textblob_sentiment import analize_sentiment

analyzer = SentimentIntensityAnalyzer()


def perform_sentiment(use_vader, sentence):
    if use_vader:
        return analyzer.polarity_scores(sentence)['compound']
    else:
        return analize_sentiment(sentence)


def get_average_sentiment_for(trees, use_vader=True, ignore_id=-1):
    tree_count = len(trees)
    analysis_sum = 0
    total_count = 0

    for i, tree in enumerate(trees):
        analysis_root = perform_sentiment(use_vader, sentence=collection.find_one({"id": tree.root.id})['text'])
        for node in tree.descendants:
            if node.is_leaf:
                if node.user_id == ignore_id and node.depth > 0:  # go to parent node and use that I think
                    tweet = collection.find_one({"id": node.parent.id})
                else:
                    tweet = collection.find_one({"id": node.id})
                result = perform_sentiment(use_vader, tweet['text']) - analysis_root  # child sentiment compared to root
                analysis_sum = analysis_sum + result
                total_count = total_count + 1
        if i % 1000 == 0:
            print("Subtree: {} children: {} average: {}".format(i, total_count, analysis_sum / total_count))
    print(
        "The total sentiment of all children is {} on a total children count of {} average: {}.".format(analysis_sum,
                                                                                                        total_count, (
                                                                                                                analysis_sum / total_count)))
    return analysis_sum / total_count


def get_sentiment_info(trees, use_vader=True, ignore_id=-1):
    tree_count = len(trees)
    total_count = 0

    sent_list = []
    response_times = []

    for i, tree in enumerate(trees):
        analysis_root = perform_sentiment(use_vader, sentence=collection.find_one({"id": tree.root.id})['text'])
        for node in tree.descendants:
            if node.is_leaf:
                if node.user_id == ignore_id and node.depth > 0:  # go to parent node and use that I think
                    tweet = collection.find_one({"id": node.parent.id})
                else:
                    tweet = collection.find_one({"id": node.id})
                result = perform_sentiment(use_vader, tweet['text'])
                delta_result = result - analysis_root  # child sentiment compared to root
                sent_list.append(delta_result)

            if node.parent is not None:
                tweet = collection.find_one({"id": node.id})
                if tweet['user']['id'] == ignore_id and node.depth > 0:
                    parent_tweet = collection.find_one({"id": node.parent.id})
                    if parent_tweet['user']['id'] != ignore_id:
                        # print("AAAAAAAAAA")

                        # print("{} to {} ".format(tweet['timestamp_ms'] ,parent_tweet['timestamp_ms'] ))

                        response_time = (int(tweet['timestamp_ms']) - int(
                            parent_tweet['timestamp_ms'])) / (1000 * 60)  # minutes
                        response_times.append(response_time)

            total_count = total_count + 1
        if i % 1000 == 0:
            print("Subtree: {} total children: {} ".format(i, total_count))

    sd = np.std(sent_list)
    mean = np.mean(sent_list)
    min = np.min(sent_list)
    max = np.max(sent_list)
    conv_length = total_count / tree_count

    negative_count = 0
    positive_count = 0
    neutral_count = 0

    response_time = None if len(response_times) == 0 else np.mean(response_times)

    for n in sent_list:
        if n < 0:
            negative_count += 1
        elif n > 0:
            positive_count += 1
        else:
            neutral_count += 1

    print("Finished total count: {}.".format(total_count))

    frq, edges = np.histogram(sent_list, 10)

    return {
        'sd': sd,
        'mean': mean,
        'min': min,
        'max': max,

        'negative_count': negative_count,
        'positive_count': positive_count,
        'neutral_count': neutral_count,

        'conv_average_size': conv_length,
        'conv_total_tweets': total_count,
        'conv_amount': tree_count,

        'response_time': response_time,
        'responses': len(response_times),

        'hist_freq': frq,
        'hist_edges': edges,

    }
