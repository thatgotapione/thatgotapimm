# -*- coding: utf-8 -*-
from nltk.corpus import twitter_samples
import codecs
from textblob import TextBlob
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import csv, re

print(twitter_samples.fileids())

pos_tweets = twitter_samples.strings('positive_tweets.json')
print(len(pos_tweets))  # Output: 5000

neg_tweets = twitter_samples.strings('negative_tweets.json')
print(len(neg_tweets))  # Output: 5000

all_tweets = twitter_samples.strings('tweets.20150430-223406.json')
print (len(all_tweets)) # Output: 20000

# positive tweets words list
pos_tweets_set = []
for tweet in pos_tweets:
    pos_tweets_set.append((tweet,1))

# negative tweets words list
neg_tweets_set = []
for tweet in neg_tweets:
    neg_tweets_set.append((tweet,-1))


def cleantweet(tmpline):
    tmpline = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z\t]) | (\w +:\/ \/\S+)", " ", tmpline).split())
    tmpline.replace("#GameOfThrones", " ")
    tmpline.replace("#GOT", " ")
    return re.sub(r"http\S+", "", tmpline)


train_set = pos_tweets_set + neg_tweets_set


# train classifier
from textblob.classifiers import NaiveBayesClassifier

print(" Training Classifier -------------------")
classifier = NaiveBayesClassifier(train_set)
print(" Training Classifier Complete -------------------")

# creating some variables to store info
polarity = 0
positive = 0
negative = 0

# Got episode tweets
got_ep_tweet_file = "/Users/krishna/PycharmProjects/thatgotapi/got-ep4.txt"


def plotDefPoints(positive, negative, total):
    labels = ['Positive [' + str(positive) + ']',
              'Negative [' + str(negative) + ']']

    print(labels)
    sizes = [positive, negative]
    colors = ['yellowgreen', 'darkred']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on GOT ' + ' by analyzing ' + str(total) + ' Tweets.')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


with codecs.open(got_ep_tweet_file, 'r', encoding='utf8') as fp:
    tweet = fp.readline()
    cnt = 1
    testset = []
    while tweet:
        tweet = cleantweet(tweet)
        blob = TextBlob(tweet, classifier=classifier)
        polarity += blob.sentiment.polarity
        cnt = cnt + 1
        if  (blob.sentiment.polarity >= 0):
            positive += 1
        elif (blob.sentiment.polarity < 0):
            negative += 1
        testset.append(tweet)
        tweet = fp.readline()

    print('Positive ' + str(positive))
    print('Negative ' + str(negative))

    print(classifier.show_informative_features(10))

    plotDefPoints(positive, negative, cnt)