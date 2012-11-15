import get_twitter_data
import baseline_classifier, naive_bayes_classifier, max_entropy_classifier, libsvm_classifier
import json,sys,pickle

keyword = 'iphone'
time = 'today'
twitterData = get_twitter_data.TwitterData()
tweets = twitterData.getTwitterData(keyword, time)

#algorithm = 'baseline'
#algorithm = 'naivebayes'
#algorithm = 'maxent'
#algorithm = 'svm'

if(len(sys.argv) < 2):
    print "Please choose the algorithm to test, sytanx = python analyze.py (svm|naivebayes|maxent)"
    exit()
    
algorithm = sys.argv[1]

if(algorithm == 'baseline'):
    bc = baseline_classifier.BaselineClassifier(tweets, keyword, time)
    bc.classify()
    val = bc.getHTML()
elif(algorithm == 'naivebayes'):    
    trainingDataFile = 'data/training_trimmed.csv'
    #trainingDataFile = 'data/full_training_dataset.csv'
    classifierDumpFile = 'data/test/naivebayes_test_model.pickle'
    trainingRequired = 1
    nb = naive_bayes_classifier.NaiveBayesClassifier(tweets, keyword, time,\
                                  trainingDataFile, classifierDumpFile, trainingRequired)
    nb.classify()
    nb.accuracy()
elif(algorithm == 'maxent'):    
    #trainingDataFile = 'data/training_trimmed.csv'
    trainingDataFile = 'data/full_training_dataset.csv'
    classifierDumpFile = 'data/test/maxent_test_model.pickle'
    trainingRequired = 1
    maxent = max_entropy_classifier.MaxEntClassifier(tweets, keyword, time,\
                                  trainingDataFile, classifierDumpFile, trainingRequired)
    #maxent.analyzeTweets()
    maxent.classify()
    maxent.accuracy()
elif(algorithm == 'svm'):    
    trainingDataFile = 'data/training_trimmed.csv'
    #trainingDataFile = 'data/full_training_dataset.csv'                
    classifierDumpFile = 'data/test/svm_test_model.pickle'
    trainingRequired = 1
    sc = libsvm_classifier.SVMClassifier(tweets, keyword, time,\
                                  trainingDataFile, classifierDumpFile, trainingRequired)
    sc.classify()
    sc.accuracy()

print 'Done'
