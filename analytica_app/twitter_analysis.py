#Python Modules
import re
from datetime import datetime

#Libraries
import pandas as pd
import numpy as np
from textblob import TextBlob
import tweepy

#Django
from django.conf import settings

#Authentication Process
auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def search_by_hashtag(q, limit=100):
    """
    Utility function to get tweets on hashtag
    returns: list of tweets
    """

    q = '#'+q.replace(' ', '_')
    tweets = tweepy.Cursor(api.search, q=q, tweet_mode='extended').items(limit)
    tweets = [{
        'tweet': tweet.full_text,
        'id': tweet.id,
        'date': tweet.created_at,
        'source': tweet.source,
        'likes': tweet.favorite_count,
        'rts': tweet.retweet_count,
        'usr_name': tweet.user.name,
        'usr_img_url': tweet.user.profile_image_url_https} for tweet in tweets if tweet.lang == 'en']
    return tweets

def df_creator(tweets):
    """
    Utility function to create data frame of tweets
    returns: data frame of tweets
    """

    data = pd.DataFrame(
        data=
        {
            'tweet': [tweet['tweet'] for tweet in tweets],
            'length': [len(tweet['tweet']) for tweet in tweets],
            'id': [tweet['id'] for tweet in tweets],
            'date': [tweet['date'] for tweet in tweets],
            'source': [tweet['source'] for tweet in tweets],
            'likes': [tweet['likes'] for tweet in tweets],
            'rts': [tweet['rts'] for tweet in tweets],
            'usr_name': [tweet['usr_name'] for tweet in tweets],
            'usr_img_url': [tweet['usr_img_url'] for tweet in tweets],            
        })
    return data

def max_calc(data):
    """
    Utility function to calculate min and max retweets or likes of set of tweets
    return: tuple of min and max values
    """

    return np.max(data)

def tweets_len_mean(tweets_lengths):
    """
    Utility function to calculate mean of length of set of tweets
    return: tuple of max and min likes
    """
    return np.mean(tweets_lengths)

def time_series_creator(data_column, date_column):
    """
    Utility function to return a time series for specific data
    """

    return pd.Series(index=date_column, data=data_column.tolist())

def clean_tweet(tweet):
    """
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    """

    return ' '.join(re.sub("(@[A-Za-z0-9])|(#.*)|(\w+:\/\/\S+)", " ", tweet).split())

def analyze_sentiment_on_tweet(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''

    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

def analyse_sentiment_on_df(df):
    """
    Utility function to classify the polarity of a tweets
    in data frame 
    """

    df['sentiment'] = np.array([ analyze_sentiment_on_tweet(tweet) for tweet in df['tweet'] ])

def get_classified_tweets(df):
    """
    Utility function to get dict of tweets classified as
    all, pos_tweets, neu_tweets and neg_tweets
    """

    all_tweets = df.pd.to_dict(orient="records")
    pos_tweets = [ tweet for tweet in all_tweets if tweet['sentiment'] < 0]
    neu_tweets = [ tweet for tweet in all_tweets if tweet['sentiment'] == 0]
    neg_tweets = [ tweet for tweet in all_tweets if tweet['sentiment'] > 0]
    return 
    {
        'all_tweets': all_tweets,
        'pos_tweets': pos_tweets,
        'neu_tweets': neu_tweets,
        'neg_tweets': neg_tweets
    }

def get_pos_tweets(df):
    """
    retrun all positive tweets
    """
    
    all_tweets = df.to_dict(orient="records")
    return [ tweet for tweet in all_tweets if tweet['sentiment'] > 0]

def get_neu_tweets(df):
    """
    retrun all neutral tweets
    """

    all_tweets = df.to_dict(orient="records")
    return [ tweet for tweet in all_tweets if tweet['sentiment'] == 0]

def get_neg_tweets(df):
    """
    retrun all negative tweets
    """

    all_tweets = df.to_dict(orient="records")
    return [ tweet for tweet in all_tweets if tweet['sentiment'] < 0]

def get_percentage_of_classified_tweets(pos_tweets, neg_tweets, neu_tweets):
    """
    Utility function to get percentage of pos_tweets, neu_tweets, neg_tweets
    """

    tweets_len = len(pos_tweets) + len(neg_tweets) + len(neu_tweets)
    return {
        'pos_tweets_percent': len(pos_tweets)*100/tweets_len,
        'neu_tweets_percent': len(neu_tweets)*100/tweets_len,
        'neg_tweets_percent': len(neg_tweets)*100/tweets_len
    }

def get_csv(df):
    """
    Utility function create csv file of data frame
    """

    df.to_csv(settings.BASE_DIR+"/csv_files/results"+str(datetime.now())+'.csv')
    return settings.BASE_DIR+"/csv_files/results"+str(datetime.now())+'.csv'
