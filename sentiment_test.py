# from graphviz import Digraph
import pprint

from nltk.sentiment import SentimentIntensityAnalyzer

from analyzer import analize_sentiment
from config import collection
from conversation import import_conversation_trees_from_db

analyzer = SentimentIntensityAnalyzer()


def perform_sentiment(use_vader, sentence):
    if use_vader:
        return analyzer.polarity_scores(sentence)['compound']
    else:
        return analize_sentiment(sentence)


def get_average_sentiment_for(trees, use_vader=True):
    tree_count = len(trees)
    analysis_sum = 0
    total_count = 0

    for i, tree in enumerate(trees):
        analysis_root = perform_sentiment(use_vader, sentence=collection.find_one({"id": tree.root.id})['text'])
        for node in tree.descendants:
            if node.is_leaf:
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
