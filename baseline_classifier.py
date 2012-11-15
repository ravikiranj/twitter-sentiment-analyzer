import sys
import re
import classifier_helper, html_helper, pickle

reload(sys)
sys.setdefaultencoding = 'utf-8'

#start class
class BaselineClassifier:
    """ Classifier using baseline method """
    #variables    
    #start __init__
    def __init__(self, data, keyword, time):
        #Instantiate classifier helper        
        self.helper = classifier_helper.ClassifierHelper('data/feature_list.txt')
        #Remove duplicates

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
    
    #start classify
    def classify(self):
        #load positive keywords file          
        inpfile = open("data/pos_mod.txt", "r")            
        line = inpfile.readline()
        positive_words = []
        while line:
            positive_words.append(line.strip())
            line = inpfile.readline()
            
        #load negative keywords file    
        inpfile = open("data/neg_mod.txt", "r")            
        line = inpfile.readline()
        negative_words = []
        while line:
            negative_words.append(line.strip())
            line = inpfile.readline()
        #start processing each tweet        
        for i in self.tweets:
            tw = self.tweets[i]
            count = 0
            res = {}
            for t in tw:
                neg_words = [word for word in negative_words if(self.string_found(word, t))]
                pos_words = [word for word in positive_words if(self.string_found(word, t))]
                if(len(pos_words) > len(neg_words)):
                    label = 'positive'
                    self.pos_count[i] += 1
                elif(len(pos_words) < len(neg_words)):
                    label = 'negative'
                    self.neg_count[i] += 1
                else:
                    if(len(pos_words) > 0 and len(neg_words) > 0):
                        label = 'positive'
                        self.pos_count[i] += 1
                    else:
                        label = 'neutral'
                        self.neut_count[i] += 1
                result = {'text': t, 'tweet': self.origTweets[i][count], 'label': label}
                res[count] = result                
                count += 1         
            #end inner loop
            self.results[i] = res
        #end outer loop   
        filename = 'data/results_lastweek.pickle'
        outfile = open(filename, 'wb')        
        pickle.dump(self.results, outfile)        
        outfile.close()
        '''
        inpfile = open('data/results_lastweek.pickle')
        self.results = pickle.load(inpfile)
        inpfile.close()
        '''
    #end
    
    #start substring whole word match
    def string_found(self, string1, string2):
        if re.search(r"\b" + re.escape(string1) + r"\b", string2):
            return True
        return False
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
    
    #start printStats
    def getHTML(self):
        return self.html.getResultHTML(self.keyword, self.results, self.time, self.pos_count, \
                                       self.neg_count, self.neut_count, 'baseline')
    #end
#end class    
