# from graphviz import Digraph
from analyzer import analize_sentiment
from config import collection
from conversation import import_conversation_trees_from_db


def get_sentiment_for(trees):
    tree_count = len(trees)
    analysis_sum = 0
    total_count = 0
    for i, tree in enumerate(trees):
        if i % 1000 == 0:
            print("[Sentiment]Processing {} of {}".format(i, tree_count))
        analysis_root = analize_sentiment(collection.find_one({"id": tree.root.id})['text'])
        for node in tree.descendants:
            if node.is_leaf:
                tweet = collection.find_one({"id": node.id})
                result = analize_sentiment(tweet['text'])
                analysis_sum = analysis_sum + result
                total_count = total_count + 1

    print(
        "The total sentiment of all children is {} on a total children count of {}.".format(analysis_sum, total_count))
