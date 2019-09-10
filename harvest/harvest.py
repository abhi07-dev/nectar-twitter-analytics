import tweepy
import re
import couchdb
import sys
import json

tweetCount = 0
limit = 0

if len(sys.argv[1]) == 2:
    limit = int(sys.argv[1])

dbuser = "admin"
dbpassword = "admin"
couchserver = couchdb.Server("http://%s:%s@localhost:5984/" % (dbuser, dbpassword))

dbname = "twitter"
if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchserver.create(dbname)

def limitTweets():
    if limit == 0:
        return True
    if tweetCount < limit:
        tweetCount += 1
        return True
    return False

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_connect(self):
        print("connected to api woohoo")

    def on_data(self, data):
        db.save(json.loads(data))
        return limitTweets()

    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        print(status)
        if status == 420:
            #returning False in on_error disconnects the stream
            return False

consumer_key = "AZKuQLLhtEiAamRWWIUJ5V5FG"
consumer_secret = "wS8Uo8daUMKSo9Dqfd9qkS7AzqADslgKgOwAtYjkbu9u0ezCgR"

access_token = "291391139-YRcTWOGDc8pv3LS9epnBEDqYLYiUXgYZHRbz3V3A"
access_token_secret = "BVnTIY7hsHDxSrhZKClXG0HllWURFlKQkn58UTgBBSARg"

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
