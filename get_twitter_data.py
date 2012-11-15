import urllib
import urllib2
import json
import datetime
import random
import pickle
from datetime import timedelta

class TwitterData:
    #start __init__
    def __init__(self):
        self.currDate = datetime.datetime.now()
        self.weekDates = []
        self.weekDates.append(self.currDate.strftime("%Y-%m-%d"))
        for i in range(1,7):
            dateDiff = timedelta(days=-i)
            newDate = self.currDate + dateDiff
            self.weekDates.append(newDate.strftime("%Y-%m-%d"))
        #end loop
    #end

    #start getWeeksData
    def getTwitterData(self, keyword, time):
        self.weekTweets = {}
        if(time == 'lastweek'):
            for i in range(0,6):
                params = {'since': self.weekDates[i+1], 'until': self.weekDates[i]}
                self.weekTweets[i] = self.getData(keyword, params)
            #end loop
            
            #Write data to a pickle file
            filename = 'data/weekTweets/weekTweets_'+urllib.unquote(keyword.replace("+", " "))+'_'+str(int(random.random()*10000))+'.txt'
            outfile = open(filename, 'wb')        
            pickle.dump(self.weekTweets, outfile)        
            outfile.close()
        elif(time == 'today'):
            for i in range(0,1):
                params = {'since': self.weekDates[i+1], 'until': self.weekDates[i]}
                self.weekTweets[i] = self.getData(keyword, params)
            #end loop
        return self.weekTweets
    '''
        inpfile = open('data/weekTweets/weekTweets_obama_7303.txt')
        self.weekTweets = pickle.load(inpfile)
        inpfile.close()
        return self.weekTweets
    '''
    #end

    #start getTwitterData
    def getData(self, keyword, params = {}):
        maxTweets = 50
        url = 'http://search.twitter.com/search.json'    
        data = {'q': keyword, 'lang': 'en', 'page': '1', 'result_type': 'recent', 'rpp': maxTweets, 'include_entities': 0}

        #Add if additional params are passed
        if params:
            for key, value in params.iteritems():
                data[key] = value
        
        params = urllib.urlencode(data)        
        try:            
            req = urllib2.Request(url, params)
            response = urllib2.urlopen(req)  
            jsonData = json.load(response)
            tweets = []
            for item in jsonData['results']:
                tweets.append(item['text'])            
            return tweets
        except urllib2.URLError, e:
            self.handleError(e)         
    #end    

    #start handleError
    def handleError(self, e):
        print e.code
        print e.read()
        return -1
    #end
#end class
