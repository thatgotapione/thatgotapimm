# -*- coding: utf-8 -*-
from nltk.corpus import twitter_samples
import codecs
from textblob import TextBlob
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import csv, re

print(twitter_samples.fileids())

# Sample Tweets
sample_pos_tweets = twitter_samples.strings('positive_tweets.json')
print(len(sample_pos_tweets))  # Output: 5000
sample_neg_tweets = twitter_samples.strings('negative_tweets.json')
print(len(sample_neg_tweets))  # Output: 5000

# Got Sample Data
positive_got_tweet_file = "/Users/krishna/PycharmProjects/thatgotapi/positive-got.txt"
negative_got_tweet_file = "/Users/krishna/PycharmProjects/thatgotapi/negative-got.txt"
neutral_got_tweet_file = "/Users/krishna/PycharmProjects/thatgotapi/neutral-got.txt"


def cleantweet(tmpline):
    tmpline = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t]) | (\w +:\/ \/\S+)", " ", tmpline).split())
    tmpline.replace("#GameOfThrones", " ")
    return re.sub(r"http\S+", "", tmpline)


def loadtweets(fileLoc,polarity,tweets):
    with codecs.open(fileLoc, 'r', encoding='utf8') as fp:
        curr=fp.readline()
        cnt = 1
        while curr:
            curr = cleantweet(curr)
            tweets.append((curr,polarity))
            print("Line {}: {}".format(cnt, curr.strip()))
            curr = fp.readline()
            cnt += 1
    return tweets


got_pos_tweets = loadtweets(positive_got_tweet_file,1,[])
got_neg_tweets = loadtweets(negative_got_tweet_file,-1,[])
got_neu_tweets = loadtweets(neutral_got_tweet_file,0,[])


train_set = got_pos_tweets + got_neg_tweets + got_neu_tweets

# train classifier
from textblob.classifiers import NaiveBayesClassifier

print(" Training Classifier -------------------")
classifier = NaiveBayesClassifier(train_set)
print(" Training Classifier Complete -------------------")

# creating some variables to store info
polarity = 0
positive = 0
negative = 0
neutral = 0

# Got Season 5 tweets
got_ep5_tweet_file = "/Users/krishna/PycharmProjects/thatgotapi/got-ep5.txt"


def plotDefPoints(positive, negative, neutral, total):
    labels = ['Positive [' + str(positive) + ']', 'Neutral [' + str(neutral) + ']',
              'Negative [' + str(negative) + ']']

    print(labels)
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'gold', 'darkred']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on GOT ' + ' by analyzing ' + str(total) + ' Tweets.')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


with codecs.open(got_ep5_tweet_file, 'r', encoding='utf8') as fp:
    tweet = fp.readline()
    cnt = 1
    while tweet:
        tweet = cleantweet(tweet)
        blob = TextBlob(tweet, classifier=classifier)
        polarity += blob.sentiment.polarity
        cnt = cnt + 1
        if (blob.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
            neutral += 1
        elif (blob.sentiment.polarity > 0):
            positive += 1
        elif (blob.sentiment.polarity < 0):
            negative += 1
        tweet = fp.readline()

    print('Positive ' + str(positive))
    print('Negative ' + str(negative))
    print('Neutral ' + str(neutral))

    plotDefPoints(positive, negative, neutral, cnt)