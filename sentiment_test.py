# from graphviz import Digraph
from analyzer import analize_sentiment
from config import collection
from conversation import import_conversation_trees_from_db


def get_sentiment_for(user_id):
    trees = import_conversation_trees_from_db(user_id)
    tree_count = len(trees)
    count = 0
    analysis_sum = 0
    for i, tree in enumerate(trees):
        analysis_tree_sum = 0
        analysis_root = analize_sentiment(collection.find_one({"id": tree.root.id})['text'])
        for node in tree.descendants:
            if i % 1000 == 0:
                print("Processing {} of {}".format(i, tree_count))
            if node.is_leaf:
                tweet = collection.find_one({"id": node.id})
                result = analize_sentiment(tweet['text'])
                analysis_sum = analysis_sum + result
                analysis_tree_sum = analysis_tree_sum + result
        if i % 1000 == 0:
            print("Root: {} tree:{}  size: {} summed: {}".format(analysis_root, i, (len(tree.descendants) + 1),
                                                                 analysis_tree_sum))
    print("The final result is {}".format(analysis_sum))



