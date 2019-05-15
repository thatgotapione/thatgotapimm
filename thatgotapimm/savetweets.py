import pandas as pd
import tweepy
import jsonpickle
import json
import time

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


print('This program saves tweets for game of thrones')

# Consume:
CONSUMER_KEY    = '<Your key here>'
CONSUMER_SECRET = '<Your key here>'

# Access:
ACCESS_TOKEN  = '<Your key here>'
ACCESS_SECRET = '<Your key here>'

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

searchquery = "#got -filter:retweets"
language_wanted = 'en'

users =tweepy.Cursor(api.search,q=searchquery,lang=language_wanted).items()
count = 0
start = 0
errorCount=0

#here we tell the program how fast to search
waitquery = 5      #this is the number of searches it will do before resting
waittime = 5.0          # this is the length of time we tell our program to rest
total_number = 5000     #this is the total number of queries we want
justincase = 1         #this is the number of minutes to wait just in case twitter throttles us



text = [0] * total_number
secondcount = 0        # No RT
idvalues = [1] * total_number
#Below is where the magic happens and the queries are being made according to our desires above
while secondcount < total_number:
    try:
        user = next(users)
        count += 1

        #We say that after every 100 searches wait 5 seconds
        if (count%waitquery == 0):
            time.sleep(waittime)
            #break

    except tweepy.TweepError:
        #catches TweepError when rate limiting occurs, sleeps, then restarts.
        #nominally 15 minnutes, make a bit longer to avoid attention.
        print ("sleeping....")
        time.sleep(60*justincase)
        user = next(users)


    except StopIteration:
        break
    try:
        #print "Writing to JSON tweet number:"+str(count)
        text_value = user._json['text']
        language = user._json['lang']
        #print(text_value)
        print(text_value)

        if "RT" not in text_value:
            if language == "en":
                text[secondcount] = text_value
                secondcount = secondcount + 1
                print("current saved is:")
                print(secondcount)

    except UnicodeEncodeError:
        errorCount += 1
        print ("UnicodeEncodeError,errorCount ="+str(errorCount))


print("Creating dataframe:")
d = {"text": text, "id": idvalues}
df = pd.DataFrame(data = d)

df.to_csv('got-test.csv', header=True, index=False, encoding='utf-8')

print ("completed")