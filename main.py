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


# create_database()  # run this only once!
# create_conversation_database()  # run this once too.

user_id = 106062176 # this is airfrance, americanair: 22536055

print("Importing trees..")
user_trees = import_conversation_trees_from_db(user_id)
print("Finding conversation length..")
conv_length = find_average_conversation_length(user_trees)
print("Average conversation length is: {}".format(conv_length))
print("Finding Sentiment score..")
get_average_sentiment_for(user_trees)  # this function gets the sentiment basically
