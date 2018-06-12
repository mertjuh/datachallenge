from config import collection
from conversation import import_conversation_trees_from_db
from sentiment_test import get_average_sentiment_for


def find_sentiment_for_ids(id_list, topics=None):
    print("Doing analysis for: {} using filter topic: {}".format(id_list, topics))
    list_length = len(id_list)
    return_info = []
    for index, id in enumerate(id_list,1):
        trees = import_conversation_trees_from_db(id,
                                                  filter=topics)
        sent_score = get_average_sentiment_for(trees)
        sent_score_with_filtered_id = get_average_sentiment_for(trees, ignore_id=id)
        result = {
            'id': id,
            'screen_name': collection.find_one({"user.id": id})['user']['screen_name'],
            'sentiment_score_old': sent_score,
            'topics': topics,
            'sentiment_score_new': sent_score_with_filtered_id
        }
        print("[{}/{}] Finished analysis for: {}".format(index, list_length, result['screen_name']))

        return_info.append(result)
    return return_info
