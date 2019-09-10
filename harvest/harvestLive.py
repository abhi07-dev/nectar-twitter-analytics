# Code adapted from https://github.com/Jefferson-Henrique/GetOldTweets-python
# to suit our needs 
import tweepy
import re
import couchdb
import sys
import json
import time
import getopt,datetime

from textblob import TextBlob
from geoSplit import *
from numpy import arange
from FindCoordinate import locateSuburb

sys.path.insert(0, "GetOldTweets-python-master")

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

consumer_key = "Qjzi0KCYqP7LsG8VCD0lDyuL8"
consumer_secret = "emtBWLfDNVZs9GZJ72Jpx4GwNHExOVCkfRJh4Kzrb6PgSJLVn7"

access_token = "3763330762-lP466X3iebmkf92SPHs7H2PbuKN2MZY3RXgXA82"
access_token_secret = "0BHG8qtiWMRKQWvx1QbiEu0CYp5NxLj9zUb49ghT662Fw"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# dirty globals
tweetCount = 0
process_id = 0
total_processes = 1
suburbHash = {}
global_lat = 0
global_lon = 0
db = None
useAPI = True
timeout = 0

def readSuburbs():
    global suburbHash
    with open("suburbs", "r") as f:
        for line in f:
            tmp = line.split()
            lat = float(tmp[0])
            lon = float(tmp[1])
            suburb = ' '.join(tmp[2:])
            suburbHash[(lat, lon)] = suburb

def getCouchServer(user, password, host):
    return couchdb.Server("http://%s:%s@%s/" % (user, password, host))

def saveTweet(tweet):
    global db, useAPI, timeout, tweetCount
    doc = {}
    try:
        doc["_id"] = tweet.id
        doc["username"] = tweet.username
        doc["text"] = tweet.text
        doc["created_at"] = tweet.date.strftime("%Y-%m-%d %H:%M:%S")
        doc["coordinates"] = [global_lon, global_lat]
        doc["suburb"] = suburbHash[(global_lat, global_lon)]
        doc["score"] = TextBlob(doc["text"]).sentiment.polarity

        if not useAPI and time.time() >= timeout:
            useAPI = True

        # USE API to get accurate coordinates
        if useAPI:
            real = api.get_status(tweet.id)
            real = json.loads(json.dumps(real._json))

            if real["coordinates"] and real["coordinates"]["coordinates"]:
                lon, lat = real["coordinates"]["coordinates"]
                doc["coordinates"] = [lon, lat]
                real["suburb"] = locateSuburb(lon, lat).lower()
                if real["suburb"] != "not available":
                    doc["suburb"] = real["suburb"]

        # SAVE TO DB        
        db.update([doc])

        tweetCount += 1
        print("(%10d tweets total)tweet from %s" % (tweetCount, doc["suburb"]))
        sys.stdout.flush()
    except tweepy.TweepError:
        print("got rate limited... not using API for 15 minutes")
        sys.stdout.flush()
        timeout = time.time() + 60 * 15
        useAPI = False
    return doc

def main(argv):

    if len(argv) == 0:
        print('You must pass some parameters. Use \"-h\" to help.')
        return

    try:
        opts, args = getopt.getopt(argv, "", ("user=", "password=", "host=", "maxtweets=", "id=", "total="))

        tweetCriteria = got.manager.TweetCriteria()
        tweetCriteria.maxTweets = 1
        tweetCriteria.since = "2018-01-01"
        global user, password, host
        for opt,arg in opts:
            if opt == '--user':
                user = arg
            if opt == '--password':
                password = arg
            if opt == '--host':
                host = arg
            if opt == '--maxtweets':
                tweetCriteria.maxTweets = int(arg)
            if opt == '--id':
                global process_id 
                process_id = int(arg)
            if opt == '--total':
                global total_processes 
                total_processes = int(arg)

        couchserver = getCouchServer(user, password, host)

        dbname = "twitter"
        global db
        if dbname in couchserver:
            db = couchserver[dbname]
        else:
            db = couchserver.create(dbname)


        readSuburbs()

        print('Searching...\n')
        sys.stdout.flush()

        def receiveBuffer(tweets):
            for t in tweets:
                if t.id not in db:
                    saveTweet(t)
                else:
                    print("tweet", t.id, "found, but already in db")
                    sys.stdout.flush()
        
        search = "geocode:%f,%f,1km"

        easyhash = 0
        while True:
            for lat in arange(lat_min, lat_max, lat_int):
                for lon in arange(long_min, long_max, long_int):
                    easyhash = (easyhash + 1) % total_processes
                    if easyhash % total_processes != process_id:
                        continue
                    if (lat, lon) in suburbHash.keys():
                        suburb = suburbHash[(lat, lon)]
                    else:
                        suburb = locateSuburb(lon, lat).lower()
                        suburbHash[(lat, lon)] = suburb
                    tweetCriteria.querySearch = search % (lat, lon)
                    if suburb == "not available":
                        continue    
                    sys.stdout.flush()
                    global global_lat, global_lon
                    global_lat = lat
                    global_lon = lon
                    got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
    finally:
        print('Done.')

if __name__ == '__main__':
    main(sys.argv[1:])
