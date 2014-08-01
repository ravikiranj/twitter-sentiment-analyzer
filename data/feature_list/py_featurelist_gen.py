import csv
import re

def process_tweet(tweet):
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
    #remove last " at string end
    tweet = tweet.rstrip('\'"')
    tweet = tweet.lstrip('\'"')
    return tweet
#end 

def uniq(list):
    l = []
    for e in list:
        if e not in l:
            l.append(e)
    return l
#end

def replaceTwoOrMore(s):
    # pattern to look for three or more repetitions of any character, including
    # newlines.
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)

inpfile = open("stopwords.txt", "r")            
line = inpfile.readline()
stopWords = []
stopWords.append('AT_USER')
stopWords.append('URL')
while line:
    word = line.strip()
    stopWords.append(word)
    line = inpfile.readline()
inpfile.close()

feature_vector = []
file1 = 'full_training_dataset.csv'
fp1 = open(file1, 'rb')
file2 = 'feature_list.txt'
fp2 = open(file2, 'w')

reader1 = csv.reader(fp1, delimiter=',', quotechar='"', escapechar='\\')
for row in reader1:
    line = []
    label = row[0]
    tweet = process_tweet(row[1])
    words = tweet.split()
    for w in words:
        w = replaceTwoOrMore(w) 
        w = w.strip('\'"?,.')
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        if(w in stopWords or val is None):
            continue
        else:
            feature_vector.append(w.lower())
#endloop
feature_vector = sorted(uniq(feature_vector))

for item in feature_vector:
    fp2.write(item+"\n")

fp1.close()
fp2.close()


    

