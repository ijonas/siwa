from nltk.sentiment.vader import SentimentIntensityAnalyzer

def find_sentiment(text):
    '''return various sentiment scores for a string of text;
    including a calculated-by-us "overall" sentiment ranging from -1 to 1'''
    sid = SentimentIntensityAnalyzer()
    sentiment = sid.polarity_scores(text)
    sentiment['overall'] = sentiment['pos'] - sentiment['neg']
    return sentiment['overall']
