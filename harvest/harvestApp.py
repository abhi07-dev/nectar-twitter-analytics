import tweepy
import re
import couchdb
import sys
import json
from textblob import TextBlob

sentimentScore = 0
tweetCount = 0
limit = 0

if len(sys.argv) == 5:
    limit = int(sys.argv[4])
elif len(sys.argv) != 4:
    sys.exit("Usage: python harvestApp.py [dbuser] [dbpassword] [host] [limit|OPTIONAL]")

dbuser = sys.argv[1]
dbpassword = sys.argv[2]
host = sys.argv[3]

couchserver = couchdb.Server("http://%s:%s@%s:5984/" % (dbuser, dbpassword, host))

dbname = "twitter"
if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchserver.create(dbname)

def limitTweets():
    global tweetCount
    tweetCount += 1
    if tweetCount == 1:
        print("%10d tweet  harvested..." % (tweetCount))
    else:
        print("%10d tweets harvested..." % (tweetCount))
    sys.stdout.flush()
    if limit == 0:
        return True
    if tweetCount < limit:
        return True
    return False

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("connected to api woohoo")
        sys.stdout.flush()

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        #print tweet on-screen
        tweet_print = tweet.encode('UTF-8')
        # print("Tweet: " + str(tweet_print))
        # to calculate sentiments using TextBlob
        tweet = TextBlob(tweet)
        # The polarity score is a float within the range [-1.0, 1.0]
        # tweetPolarity = tweet.sentiment.polarity
        # print("Tweet Polarity: " + str(tweetPolarity))
        # global sentimentScore
        # sentimentScore += tweetPolarity
        # print("Cumulative Sentiment Score: " + str(sentimentScore))
        all_data["score"] = tweet.sentiment.polarity
        db.save(all_data)
        return limitTweets()

    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        print(status)
        if status == 420:
            #returning False in on_error disconnects the stream
            return False

consumer_key = "Qjzi0KCYqP7LsG8VCD0lDyuL8"
consumer_secret = "emtBWLfDNVZs9GZJ72Jpx4GwNHExOVCkfRJh4Kzrb6PgSJLVn7"

access_token = "3763330762-lP466X3iebmkf92SPHs7H2PbuKN2MZY3RXgXA82"
access_token_secret = "0BHG8qtiWMRKQWvx1QbiEu0CYp5NxLj9zUb49ghT662Fw"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# try:
#     redirect_url = auth.get_authorization_url()
# except tweepy.TweepError:
#     print('Error! Failed to get request token.')

# print(redirect_url)
# # Example w/o callback (desktop)
# pattern = r'.*oauth_token=([\w]+)'
# m = re.match(pattern, redirect_url)
# token = m.group(1)
# print(token)
# verifier = input('Verifier:')

# auth.request_token = { 'oauth_token' : token,
#                          'oauth_token_secret' : verifier }

# try:
#     auth.get_access_token(verifier)
# except tweepy.TweepError:
#     print('Error! Failed to get access token.')

# print(auth.access_token)
# print(auth.access_token_secret)

api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# melbourne bounding box coordinates
# for other locations use :
# https://boundingbox.klokantech.com/
myStream.filter(locations = [144.5937,-38.4339,145.5125,-37.5113])
