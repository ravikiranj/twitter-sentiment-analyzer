import json,sys
sys.path.append("/home/ravikirn/lib64/python/")
sys.path.append("/home/ravikirn/lib/python/")
sys.path.append("/home/ravikirn/coursework/data-mining/packages/libsvm-3.12/python/")

import get_twitter_data
import baseline_classifier, naive_bayes_classifier, max_entropy_classifier, libsvm_classifier,pickle

keyword = 'iphone'
time = 'today'
#twitterData = get_twitter_data.TwitterData()
#tweets = twitterData.getTwitterData(keyword, time)
infile = open('data/tweets_current.pickle')
tweets = pickle.load(infile)
infile.close()

#algorithm = 'baseline'
#algorithm = 'naivebayes'
#algorithm = 'maxent'
#algorithm = 'svm'

if(len(sys.argv) < 2): 
    print "Please choose the algorithm to test, syntax = python analyze.py (svm|naivebayes|maxent)"
    exit()
    
algorithm = sys.argv[1]
if(algorithm == 'baseline'):
    bc = baseline_classifier.BaselineClassifier(tweets, keyword, time)
    bc.classify()
    val = bc.getHTML()
elif(algorithm == 'naivebayes'):
    #trainingDataFile = 'data/training_trimmed.csv'
    trainingDataFile = 'data/full_training_dataset.csv'
    classifierDumpFile = 'data/test/naivebayes_test_model.pickle'
    trainingRequired = 1
    print 'Started to instantiate Naive Bayes Classifier'
    sys.stdout.flush()
    nb = naive_bayes_classifier.NaiveBayesClassifier(tweets, keyword, time,\
                                  trainingDataFile, classifierDumpFile, trainingRequired)
    #nb.classify()
    print 'Computing Accuracy'
    sys.stdout.flush()
    nb.accuracy()
elif(algorithm == 'maxent'):
    #trainingDataFile = 'data/training_trimmed.csv'
    trainingDataFile = 'data/full_training_dataset.csv'
    classifierDumpFile = 'data/test/maxent_test_model.pickle'
    trainingRequired = 1
    print 'Started to instantiate Max Entropy Classifier'
    sys.stdout.flush()
    maxent = max_entropy_classifier.MaxEntClassifier(tweets, keyword, time,\
                                  trainingDataFile, classifierDumpFile, trainingRequired)
    #maxent.analyzeTweets()
    #maxent.classify()
    print 'Computing Accuracy'
    sys.stdout.flush()
    maxent.accuracy()
elif(algorithm == 'svm'):
    #trainingDataFile = 'data/training_trimmed.csv'
    trainingDataFile = 'data/full_training_dataset.csv'
    classifierDumpFile = 'data/test/svm_test_model.pickle'
    trainingRequired = 1
    print 'Started to instantiate SVM Classifier'
    sys.stdout.flush()
    sc = libsvm_classifier.SVMClassifier(tweets, keyword, time,\
                                  trainingDataFile, classifierDumpFile, trainingRequired)
    #sc.classify()
    print 'Computing Accuracy'
    sys.stdout.flush()
    sc.accuracy()
print 'Done'
sys.stdout.flush()

