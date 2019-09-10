import tweepy
import re
import couchdb
import sys
import json
from textblob import TextBlob

sentimentScore = 0
tweetCount = 0
limit = 10
start = 0

if len(sys.argv) == 5 or len(sys.argv) == 6:
    limit = int(sys.argv[4])
    start = int(sys.argv[5])
elif len(sys.argv) != 4:
    sys.exit("Usage: python harvestApp.py [dbuser] [dbpassword] [host] [limit|OPTIONAL]")

dbuser = sys.argv[1]
dbpassword = sys.argv[2]
host = sys.argv[3]

couchserver = couchdb.Server("http://%s:%s@%s/" % (dbuser, dbpassword, host))

dbname = "more_tweets"
if dbname in couchserver:
    db = couchserver[dbname]
else:
    db = couchserver.create(dbname)

db2user = "readonly"
db2password = "ween7ighai9gahR6"
view = "twitter/geoindex"

couchserver2 = couchdb.Server("http://%s:%s@45.113.232.90/couchdbro/" % (db2user, db2password))

db2name = "twitter"
db2 = couchserver2[db2name]

for item in db2.view(view, limit=limit, reduce=False, skip=start, startkey=["r1r0", {}]):
    doc = item.value

    tweet = doc["properties"]["text"]
    tweet_print = tweet.encode('UTF-8')
    tweet = TextBlob(tweet)
    
    # The polarity score is a float within the range [-1.0, 1.0]
    doc["score"] = tweet.sentiment.polarity
    # To make compatible with other tweets, store tweet twice under doc['text']
    doc["text"] = doc["properties"]["text"]
    doc["_id"] = item.id
    tweetCount += 1
    print("(%10d tweets total)tweet from %s" % (tweetCount, doc["properties"]["location"]))
    sys.stdout.flush()
    db.update([doc])
