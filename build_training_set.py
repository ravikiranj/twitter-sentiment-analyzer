import classifier_helper
from classifier_helper import *
  
'''
inpfile = open("training.1600000.processed.noemoticon.csv", "r")
line = inpfile.readline()
maxCount = 100
count = 1
tweets = []
while line:    
    count += 1
    if count > maxCount:
        break    
    splitArr = line.split(',"')
    unprocessed_tweet = splitArr[5]
    #tweet = process_tweet(unprocessed_tweet)
    tweet = process_tweet_modified(unprocessed_tweet)    
    tweets.append(tweet)    
    line = inpfile.readline()
#end while loop
'''
inpfile = open("baseline_output.txt", "r")
line = inpfile.readline()
count = 1
tweetItems = []
opinions = []
while line:    
    count += 1
    splitArr = line.split('|')
    processed_tweet = splitArr[0].strip()
    opinion = splitArr[1].strip()
    tweet_item = processed_tweet, opinion
    if(opinion != 'neutral' and opinion != 'negative' and opinion != 'positive'):
        print('Error with tweet = %s, Line = %s') % (processed_tweet, count)
    tweetItems.append(tweet_item)    
    line = inpfile.readline()
#end while loop

tweets = []    
for (words, sentiment) in tweetItems:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

word_features = get_word_features(get_words_in_tweets(tweets))
set_word_features(word_features)
training_set = nltk.classify.apply_features(extract_features, tweets)
    
classifier = nltk.NaiveBayesClassifier.train(training_set)
tweet = 'im so sad'
print classifier.classify(extract_features(tweet.split()))
print nltk.classify.accuracy(classifier, training_set)
classifier.show_most_informative_features(20)
    
