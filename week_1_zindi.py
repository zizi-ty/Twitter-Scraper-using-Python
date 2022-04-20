# -*- coding: utf-8 -*-
"""Week 1 - Zindi

# Collecting tweets based on key words

This notebook shows you how to use the [tweepy](https://www.tweepy.org/) python library to collect tweets from Twitter based on key words.
"""

"""STEP 1: PYTHON PACKAGES INSTALLATION

    Install the following python packages that will help you to collect data from twitter.com"""

!pip install tweepy

!pip install unidecode

"""STEP 2: IMPORT IMPORTANT PACKAGES """

#import dependencies
import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from unidecode import unidecode
import time
import datetime
from tqdm import tqdm 
import pandas as pd  
import numpy as np

"""STEP 3: AUTHENTICATING TO TWITTER'S API"""

consumer_key = 'your consumer key'
consumer_secret = 'your secret key'

access_token = 'your access token'
access_secret = 'your access secret'

"""STEP 4:  CONNECT TO TWITTER API USING THE SECRET KEY AND ACCESS TOKEN"""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

"""STEP 5: DEFINE A FUNCTION THAT WILL TAKE OUR SEARCH QUERY"""

def tweetSearch(query, limit):
    """
    This function will search a query provided in the twitter and,
    retun a list of all tweets that have a query. 
    """

    # Create a blank variable
    tweets = []

    # Iterate through Twitter using Tweepy to find our query with our defined limit
    for page in tweepy.Cursor(
        api.search, q=query, count=limit, tweet_mode="extended"
    ).pages(limit):
        for tweet in page:
            tweets.append(tweet)

    # return tweets
    return tweets

"""STEP 6: CREATE A FUNCTION TO SAVE TWEETS INTO A DATAFRAME"""

def tweets_to_data_frame(tweets):
    """
    This function will receive tweets and collect specific data from it such as place, tweet's text,likes 
    retweets and save them into a pandas data frame.
    
    This function will return a pandas data frame that contains data from twitter.
    """
    df = pd.DataFrame(data=[tweet.full_text.encode('utf-8') for tweet in tweets], columns=["Tweets"])

    df["id"] = np.array([tweet.id for tweet in tweets])
    df["lens"] = np.array([len(tweet.full_text) for tweet in tweets])
    df["date"] = np.array([tweet.created_at for tweet in tweets])
    df["place"] = np.array([tweet.place for tweet in tweets])
    df["coordinateS"] = np.array([tweet.coordinates for tweet in tweets])
    df["lang"] = np.array([tweet.lang for tweet in tweets])
    df["source"] = np.array([tweet.source for tweet in tweets])
    df["likes"] = np.array([tweet.favorite_count for tweet in tweets])
    df["retweets"] = np.array([tweet.retweet_count for tweet in tweets])

    return df

"""STEP 7: ADD TWITTER HASHTAGS RELATED TO GENDER-BASED VIOLENCE"""

# add hashtags in the following list
hashtags = [
'#GBV',
'#sexism',
'#rape'    
]

"""STEP 8: RUN BOTH FUNCTIONS TO COLLECT DATA FROM TWITTER RELATED TO THE HASHTAGS LISTED ABOVE"""

total_tweets = 0

"""
The following for loop will collect a tweets that have the hashtags
 mentioned in the list and save the tweets into csv file
"""

for n in tqdm(hashtags):
    # first we fetch all tweets that have specific hashtag
    hash_tweets = tweetSearch(query=n,limit=7000)
    total_tweets += int(len(hash_tweets))
    
    # second we convert our tweets into datarame
    df = tweets_to_data_frame(hash_tweets)
    
    #third we save the dataframe into csv file
    df.to_csv("tweets.csv".format(n))

df

# show total number of tweets collected
print("total_tweets: {}".format(total_tweets))

"""For more tweepy configuration please read the tweepy documentation [here](https://docs.tweepy.org/en/latest/)"""
