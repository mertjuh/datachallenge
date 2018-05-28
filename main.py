import conversation
import databaseimporter as importer

from config import jsonDirectory
from conversation import find_conversation_length, import_conversation_trees_from_db
from sentiment_test import get_sentiment_for


def create_database():
    importer.create_indexes()
    importer.process_all_json_files(jsonDirectory)
    importer.sanitize_db()


def create_conversation_database():
    conversation.create_indexes()
    conversation.import_all_trees_to_db()


#create_database()  # run this only once.
#create_conversation_database()  # run this once too.

user_id = 22536055
find_conversation_length(import_conversation_trees_from_db(user_id))
#get_sentiment_for(user_id)  # this function gets the sentiment basically
