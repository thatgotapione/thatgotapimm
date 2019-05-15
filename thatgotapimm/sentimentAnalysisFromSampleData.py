#import nltk
#nltk.download('twitter_samples')

from nltk.corpus import twitter_samples
from textblob import TextBlob

print (twitter_samples.fileids())

pos_tweets = twitter_samples.strings('positive_tweets.json')
print(len(pos_tweets))  # Output: 5000

neg_tweets = twitter_samples.strings('negative_tweets.json')
print(len(neg_tweets))  # Output: 5000

all_tweets = twitter_samples.strings('tweets.20150430-223406.json')
print (len(all_tweets)) # Output: 20000

# positive tweets words list
pos_tweets_set = []
for tweet in pos_tweets:
    pos_tweets_set.append((tweet,'pos'))

# negative tweets words list
neg_tweets_set = []
for tweet in neg_tweets:
    neg_tweets_set.append((tweet,'neg'))

print(len(pos_tweets_set), len(neg_tweets_set))  # Output: (5000, 5000)

train_set = pos_tweets_set[:500] + neg_tweets_set[:500]
test_set = pos_tweets_set[500:1000] + neg_tweets_set[500:1000]

# train classifier
from textblob.classifiers import NaiveBayesClassifier
print(" Training Classifier -------------------")
classifier = NaiveBayesClassifier(train_set)
print(" Training Classifier Complete -------------------")


for tweet in all_tweets[:20]:
    blob = TextBlob(tweet,classifier=classifier)
    print (blob)
    print (blob.classify())




# calculate accuracy
#print(" Running Classifier on Test Set -------------------")
#accuracy = classifier.accuracy(test_set)
#print(" Running Classifier on Test Set Complete-------------------")
#print(accuracy)  # Output: 0.727

# show most frequently occurring words
#print(classifier.show_informative_features(10))