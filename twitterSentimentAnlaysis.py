import tweepy
import codecs
from string import punctuation

# encoding scheme for reading and writing unicode data
encoding = 'utf-8'

__author__ = "Manoj KV"


class SentimentAnalysis:

    def __init__(self):
        """
        Initialize Credentials to connect twitter API
        """
        credentials = {
            "twitter": dict(consumer_key="xxxxxxxxxxxxxxxxxxxxxxxxxx",
                            consumer_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                            access_token="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                            access_token_secret="xxxxxxxxxxxxxxxxxxxxxxxxxxx")
        }

        oauth_data = credentials["twitter"]  # hardcoded handle for public tweets is sufficient
        auth = tweepy.OAuthHandler(oauth_data["consumer_key"], oauth_data["consumer_secret"])
        auth.set_access_token(oauth_data["access_token"], oauth_data["access_token_secret"])

        self.api = tweepy.API(auth)

        self.positive_words = open("positive_words.txt").read().split('\n')
        # print self.positive_words
        self.negative_words = open("negative_words.txt").read().split('\n')
        # print self.negative_words

    def celebritysearch(self, name):
        """
        get all the tweets about the celebrities and writing into a text file
        :rtype: object
        :param name: 
        :return: 
        """
        output_file = codecs.open("public_tweets.txt", 'w', "utf-8")
        public_tweets = self.api.search(q=name, lang="en", locale="en", count=1000)

        for tweet in public_tweets:
            output_file.write(tweet.text + '\n')

        output_file.close()

    def words_count(self, tweets):
        """
        get the number of words present in the tweet
        :param tweets: 
        :return: 
        """
        positive_count = 0
        negative_count = 0

        for punc in list(punctuation):
            tweet = tweets.replace(punc, '')
            words = tweet.lower().split(' ')

        for word in words:
            if word in self.positive_words:
                positive_count = positive_count + 1
                # print word
            elif word in self.negative_words:
                negative_count = negative_count + 1
                # print word

        return positive_count, negative_count

    def sentiment(self):
        # type: () -> object
        # type: () -> object
        """
        Get all the tweets from "public_tweets.txt" and create a list file
        and then Print the Sentiment Result
        :rtype: object
        :param: 
        :return: 
        """
        tweets_list = codecs.open("public_tweets.txt", 'r', "utf-8").read().split('\n')
        pos_cnt = 0
        neg_cnt = 0

        # Get the word count on each tweet stored in list
        for tweet in tweets_list:
            if len(tweet):
                pos, neg = self.words_count(tweet)
                # print pos, neg
                pos_cnt = pos_cnt + pos
                neg_cnt = neg_cnt + neg

        # Logic to decide the sentiment result
        if pos_cnt > neg_cnt:
            return "Positive"
        elif pos_cnt < neg_cnt:
            return "Negative"
        else:
            return "Neutral"
"""
if __name__ == '__main__':
    celebrity = SentimentAnalysis()
    celebrity.celebritysearch('MS Dhoni')
    celebrity.sentiment()
"""
