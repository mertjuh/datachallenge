from textblob import TextBlob
import re
import numpy as np


def clean_text(text):
    '''
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())


def analize_sentiment(text):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_text(text))
    return analysis.sentiment.polarity  # I think this should be fine? ..
    '''if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1
    '''

# We create a column with the result of the analysis:
# df['SA'] = np.array([analize_sentiment(text) for text in df['text']])

# We display the updated dataframe with the new column:
# df[['text', 'SA']]
# We count the amount of positive, neutral and negative tweets:
# df['SA'].value_counts()
