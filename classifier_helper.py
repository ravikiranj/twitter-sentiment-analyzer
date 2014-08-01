import re
import nltk
from nltk.classify import *

class ClassifierHelper:
    #start __init__
    def __init__(self, featureListFile):
        self.wordFeatures = []
        # Read feature list
        inpfile = open(featureListFile, 'r')
        line = inpfile.readline()        
        while line:
            self.wordFeatures.append(line.strip())
            line = inpfile.readline()
    #end    

    #start extract_features
    def extract_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.wordFeatures:
            word = self.replaceTwoOrMore(word) 
            word = word.strip('\'"?,.')
            features['contains(%s)' % word] = (word in document_words)
        return features
    #end

    #start replaceTwoOrMore
    def replaceTwoOrMore(self, s):
        # pattern to look for three or more repetitions of any character, including
        # newlines.
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
        return pattern.sub(r"\1\1", s)
    #end

    def getSVMFeatureVectorAndLabels(self, tweets):
        sortedFeatures = sorted(self.wordFeatures)
        map = {}
        feature_vector = []
        labels = []
        for t in tweets:
            label = 0
            map = {}
            #Initialize empty map
            for w in sortedFeatures:
                map[w] = 0
            
            tweet_words = t[0]
            tweet_opinion = t[1]
            #Fill the map
            for word in tweet_words:
                word = self.replaceTwoOrMore(word) 
                word = word.strip('\'"?,.')
                if word in map:
                    map[word] = 1
            #end for loop
            values = map.values()
            feature_vector.append(values)
            if(tweet_opinion == 'positive'):
                label = 0
            elif(tweet_opinion == 'negative'):
                label = 1
            elif(tweet_opinion == 'neutral'):
                label = 2
            labels.append(label)            
        return {'feature_vector' : feature_vector, 'labels': labels}
    #end
    
    #start getSVMFeatureVector
    def getSVMFeatureVector(self, tweets):
        sortedFeatures = sorted(self.wordFeatures)
        map = {}
        feature_vector = []
        for t in tweets:
            label = 0
            map = {}
            #Initialize empty map
            for w in sortedFeatures:
                map[w] = 0
            #Fill the map
            for word in t:
                if word in map:
                    map[word] = 1
            #end for loop
            values = map.values()
            feature_vector.append(values)                    
        return feature_vector
    #end
    
    #start process_tweet
    def process_tweet(self, tweet):
        #Conver to lower case
        tweet = tweet.lower()
        #Convert https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)    
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip()
        #remove first/last " or 'at string end
        tweet = tweet.rstrip('\'"')
        tweet = tweet.lstrip('\'"')
        return tweet
    #end 
    
    #start is_ascii
    def is_ascii(self, word):
        return all(ord(c) < 128 for c in word)
    #end
#end class
