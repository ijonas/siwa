#standard library
import time, os
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta

#third party libs
import tweepy, nltk

#our stuff
import constants as c
from feeds.data_feed import DataFeed
from feeds.twitter import sentiment_analyzer #libs we wrote

#set twitter bearer_token in environment or replace with your bearer_token
bearer_token = os.environ.get('twitter_bearer_token', None)
if bearer_token is None: 
    print('\033[31;1mNo twitter bearer token found; either set a `twitter_bearer_token` \
 environment variable or assign in feeds/twitter/twitter.py \033[0m')

class STREAM_API(tweepy.StreamingClient):
    tweet_count = 0
    def on_tweet(self, tweet):
        '''handle tweet; i.e. find sentiment, update queue with latest value'''
        tweet_time = time.time() #note: tweet.created_at is None for some reason.
        self.tweet_count += 1
        sentiment = sentiment_analyzer.find_sentiment(tweet.text)
        self.SENTIMENT_BUFFER.append(sentiment)
        if len(self.SENTIMENT_BUFFER) == 5:
            #only add datapoint if we have 5 tweets to average sentiment across
            self.DATAPOINT_DEQUE.append(sum(self.SENTIMENT_BUFFER)/len(self.SENTIMENT_BUFFER))
        
        #TODO SEND TO QUEUE

    def delete_all_rules(self):
        ''' clear all rules (stored twitter-side);
        max # of rules on 'Essential' twitter API access level is 5,
        so you must delete some or all rules to add others;
        https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api#v2-access-level
        '''
        response=self.get_rules()
        rule_list = response.data
        if rule_list != None:
            ids = [rule.id for rule in rule_list]
            self.delete_rules(ids)

    #TODO handle ratelimiting errors
    #tweepy will automatically reconnect and "handle" the error,
    #so it will self-correct and resume producing data,
    #but we may want to flag the feed as paused or something.

class Twitter(DataFeed):
    NAME = 'twitter'
    ID = 7 #
    HEARTBEAT = 1 #irrelevant for a twitter stream?
    DATAPOINT_DEQUE = deque([], maxlen=100)
    SENTIMENT_BUFFER = deque([], maxlen=5)
    RULES_TO_MONITOR = ['bitcoin OR litecoin',] #@raoulGMI

    TWITTER_STREAM = STREAM_API(bearer_token = bearer_token)#,
    TWITTER_STREAM.DATAPOINT_DEQUE = DATAPOINT_DEQUE
    TWITTER_STREAM.SENTIMENT_BUFFER = SENTIMENT_BUFFER

    #Feed-specific class-level attrs

    @classmethod
    def stop(cls):
        x=cls.TWITTER_STREAM.disconnect()
        cls.ACTIVE = False

    @classmethod
    def run(cls):
        #NOTE: you can have max 5 rules with Essential API access
        #however, each rule can have many terms, the below is ONE rule not 3, for example
        #https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule

        #CHECK LIST OF RULES TO MONITOR
        #UPDATE (add/delete new/old rules) AS NEEDED:
        rules_to_monitor = cls.RULES_TO_MONITOR
        rules_to_add = [rule for rule in rules_to_monitor] # copy
        rules_to_delete = list()

        current_rules = cls.TWITTER_STREAM.get_rules()
        for rule in current_rules.data:
            if not rule.value in rules_to_monitor:
                rules_to_delete.append(rule.id)
            else:
                rules_to_add.remove(rule.value)

        if rules_to_delete:
            #ONLY delete superfluous rules
            #this is so we dont just delete_all() every time
            #and hit an API rate limit while testing
            if c.DEBUG: print('unused twitter rules found; deleting')
            cls.TWITTER_STREAM.delete_rules(rules_to_delete)

        if rules_to_add:
            #add new rules
            if c.DEBUG: print('new twitter rules found; adding')
            cls.TWITTER_STREAM.add_rules([tweepy.StreamRule(rule) for rule in rules_to_add])

        #this is the loop:
        cls.TWITTER_STREAM.filter()

    @classmethod
    def get_latest_source_data(cls):
        ''' fetch data from datasource; in this case, the blockchain'''
        #TODO TBD: return None if datum already seen?
        pass