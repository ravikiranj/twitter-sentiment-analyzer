import nltk.classify
import re, pickle, csv, os
import classifier_helper, html_helper


from collections import defaultdict

#start class
class MaxEntClassifier:
    """ Maximum Entropy Classifier """
    #variables    
    #start __init__
    def __init__(self, data, keyword, time, trainingDataFile, classifierDumpFile, trainingRequired = 0):
        #Instantiate classifier helper        
        self.helper = classifier_helper.ClassifierHelper('data/feature_list.txt')
        
        self.lenTweets = len(data)
        self.origTweets = self.getUniqData(data)
        self.tweets = self.getProcessedTweets(self.origTweets)
        
        self.results = {}
        self.neut_count = [0] * self.lenTweets
        self.pos_count = [0] * self.lenTweets
        self.neg_count = [0] * self.lenTweets

        self.time = time
        self.keyword = keyword
        self.html = html_helper.HTMLHelper()
        self.trainingDataFile = trainingDataFile
        
        #call training model
        if(trainingRequired):
            self.classifier = self.getMaxEntTrainedClassifer(trainingDataFile, classifierDumpFile)
        else:
            f1 = open(classifierDumpFile)            
            if(f1):
                self.classifier = pickle.load(f1)                
                f1.close()                
            else:
                self.classifier = self.getMaxEntTrainedClassifer(trainingDataFile, classifierDumpFile)
    #end
            #start getUniqData
    def getUniqData(self, data):
        uniq_data = {}        
        for i in data:
            d = data[i]
            u = []
            for element in d:
                if element not in u:
                    u.append(element)
            #end inner loop
            uniq_data[i] = u            
        #end outer loop
        return uniq_data
    #end
    
    #start getProcessedTweets
    def getProcessedTweets(self, data):        
        tweets = {}        
        for i in data:
            d = data[i]
            tw = []
            for t in d:
                tw.append(self.helper.process_tweet(t))
            tweets[i] = tw            
        #end loop
        return tweets
    #end
    
    #start getMaxEntTrainedClassifier
    def getMaxEntTrainedClassifer(self, trainingDataFile, classifierDumpFile):        
        # read all tweets and labels
        # maxItems = 0 indicates read all training data
        maxItems = 0 
        tweetItems = self.getFilteredTrainingData(trainingDataFile, maxItems)
        
        tweets = []
        for (words, sentiment) in tweetItems:
            words_filtered = [e.lower() for e in words.split() if(self.helper.is_ascii(e))]
            tweets.append((words_filtered, sentiment))
                    
        training_set = nltk.classify.apply_features(self.helper.extract_features, tweets)
        # Write back classifier        
        classifier = nltk.classify.maxent.MaxentClassifier.train(training_set, 'GIS', trace=3, \
                                    encoding=None, labels=None, sparse=True, gaussian_prior_sigma=0, max_iter = 5) 
        outfile = open(classifierDumpFile, 'wb')        
        pickle.dump(classifier, outfile)        
        outfile.close()        
        return classifier
    #end
    
    #start getFilteredTrainingData
    def getFilteredTrainingData(self, trainingDataFile, maxItems = 0):
        #maxItems = 0 indicates read all training data
        fp = open( trainingDataFile, 'rb' )
        if(maxItems == 0):
            min_count = self.getMinCount(trainingDataFile)        
        else:
            min_count = maxItems
        min_count = 40000
        neg_count, pos_count, neut_count = 0, 0, 0
        
        reader = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
        tweetItems = []
        count = 1       
        for row in reader:
            processed_tweet = self.helper.process_tweet(row[1])
            sentiment = row[0]
            
            if(sentiment == 'neutral'):                
                if(neut_count == int(min_count)):
                    continue
                neut_count += 1
            elif(sentiment == 'positive'):
                if(pos_count == min_count):
                    continue
                pos_count += 1
            elif(sentiment == 'negative'):
                if(neg_count == min_count):
                    continue
                neg_count += 1
            
            tweet_item = processed_tweet, sentiment
            tweetItems.append(tweet_item)
            count +=1
        #end loop
        return tweetItems
    #end 
    
    #start getMinCount
    def getMinCount(self, trainingDataFile):
        fp = open( trainingDataFile, 'rb' )
        reader = csv.reader( fp, delimiter=',', quotechar='"', escapechar='\\' )
        neg_count, pos_count, neut_count = 0, 0, 0
        for row in reader:
            sentiment = row[0]
            if(sentiment == 'neutral'):
                neut_count += 1
            elif(sentiment == 'positive'):
                pos_count += 1
            elif(sentiment == 'negative'):
                neg_count += 1
        #end loop
        return min(neg_count, pos_count, neut_count)
    #end
    
        #start classify
    def classify(self):        
        for i in self.tweets:
            tw = self.tweets[i]
            count = 0
            res = {}
            for t in tw:
                label = self.classifier.classify(self.helper.extract_features(t.split()))
                if(label == 'positive'):
                    self.pos_count[i] += 1
                elif(label == 'negative'):                
                    self.neg_count[i] += 1
                elif(label == 'neutral'):                
                    self.neut_count[i] += 1
                result = {'text': t, 'tweet': self.origTweets[i][count], 'label': label}
                res[count] = result
                count += 1
            #end inner loop
            self.results[i] = res
        #end outer loop
    #end

    #start accuracy
    def accuracy(self):
        maxItems = 0
        tweets = self.getFilteredTrainingData(self.trainingDataFile)
        total = 0
        correct = 0
        wrong = 0
        self.accuracy = 0.0
        for (t, l) in tweets:
            label = self.classifier.classify(self.helper.extract_features(t.split()))
            if(label == l):
                correct+= 1
            else:
                wrong+= 1
            total += 1
        #end loop
        self.accuracy = (float(correct)/total)*100
        print 'Total = %d, Correct = %d, Wrong = %d, Accuracy = %.2f' % \
                                                (total, correct, wrong, self.accuracy)        
    #end

    #start analyzeTweets
    def analyzeTweets(self):
        tweets = self.getFilteredTrainingData(self.trainingDataFile)
        d = defaultdict(int)
        for (t, l) in tweets:
            for word in t.split():
                d[word] += 1
        #end loop
        for w in sorted(d, key=d.get, reverse=True):
            print w, d[w]
    #end

    #start writeOutput
    def writeOutput(self, filename, writeOption='w'):
        fp = open(filename, writeOption)
        for i in self.results:
            res = self.results[i]
            for j in res:
                item = res[j]
                text = item['text'].strip()
                label = item['label']
                writeStr = text+" | "+label+"\n"
                fp.write(writeStr)
            #end inner loop
        #end outer loop      
    #end writeOutput    
    
    #start getHTML
    def getHTML(self):
        return self.html.getResultHTML(self.keyword, self.results, self.time, self.pos_count, \
                                       self.neg_count, self.neut_count, 'maxentropy')
    #end
#end class
