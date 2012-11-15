import urllib
import datetime
from datetime import timedelta 

class HTMLHelper:
    #start __init__
    def __init__(self):
        self.html = ''
        self.currDate = datetime.datetime.now()
        self.weekDates = []
        #self.weekDates.append(self.currDate.strftime("%Y-%m-%d"))
        self.weekDates.append(self.currDate.strftime("%b %d"))
        for i in range(1,7):
            dateDiff = timedelta(days=-i)
            newDate = self.currDate + dateDiff
            #self.weekDates.append(newDate.strftime("%Y-%m-%d"))
            self.weekDates.append(newDate.strftime("%b %d"))
    #end
        
    #start getDefaultHTML
    def getDefaultHTML(self, error = 0):
        html = '''
<html>
<head><title>Twitter Sentiment Analysis</title>
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/3.4.1/build/cssgrids/grids-min.css" />
    <link rel="stylesheet" type="text/css" href="static/styles.css" />
</head>
<body>
    <div class="yui3-g" id="doc">
    <div class="yui3-u" id="hd">
        <h2> Twitter Sentiment Analyzer </h2>
    </div>
    <div class="yui3-u" id="bd">
        <form name="keyform" id="key-form" method="get" onSubmit="return checkEmpty(this);">
        <p><input type="text" value="" name="keyword" id="keyword"/><input type="submit" value="Submit" id="sub"/></p>
            <div id="timeframe">            
                <input type="radio" name="time" id="today" value="today" checked="true">Today</input>
                <input type="radio" name="time" id="lastweek" value="lastweek">Last 7 days</input>
            </div>
            <div id="choice">
                <input type="radio" name="method" id="baseline" value="baseline" checked="true">Baseline</input>
                <input type="radio" name="method" id="naivebayes" value="naivebayes">Naive Bayes</input>
                <input type="radio" name="method" id="maxentropy" value="maxentropy">Maximum Entropy</input>
                <input type="radio" name="method" id="svm" value="svm">Support Vector Machine</input>
            </div>
        </form>
'''
        if(error == 1):
            html += '<div id="error">Unable to fetch TWitter API data. Please try again later.</div>'
        elif(error == 2):
            html += '<div id="error">Unrecognized Method of Classfication, please choose one from above.</div>'
        html += '''
    </div>
    <div id='ft'>by Ravikiran Janardhana</div>
    <script type="text/javascript">
    function checkEmpty(f) {
        if (f.keyword.value === "") {
            alert('Please enter a valid keyword');
            return false;
        }else{
            f.submit();
            return true;
        }
    }
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-31119754-1']);
    _gaq.push(['_trackPageview']);
    
    (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();
    </script>
</body>
</html>
'''
        return html
    #end
    
    #start getResultHTML
    def getResultHTML(self, keyword, results, time, pos_count, neg_count, neut_count, checked):
        keyword = urllib.unquote(keyword.replace("+", " "))
        html = '''
<html>
<head><title>Twitter Sentiment Analysis</title>
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/3.4.1/build/cssgrids/grids-min.css" />
    <link rel="stylesheet" type="text/css" href="static/styles.css" />
</head>
<body>
    <div class="yui3-g" id="doc">
    <div class="yui3-u" id="hd">
        <h2> Twitter Sentiment Analyzer </h2>
    </div>
    <div class="yui3-u" id="bd">        
        <form name="keyform" id="key-form" method="get" onSubmit="return checkEmpty(this);">
        <p><input type="text" value="" name="keyword" id="keyword"/><input type="submit" value="Search" id="sub"/></p>        
        <div id="timeframe">            
                <input type="radio" name="time" id="today" value="today" checked="true">Today</input>
                <input type="radio" name="time" id="lastweek" value="lastweek">Last 7 days</input>
        </div>
        <div id="choice">
            <input type="radio" name="method" id="baseline" value="baseline">Baseline</input>
            <input type="radio" name="method" id ="naivebayes" value="naivebayes">Naive Bayes</input>
            <input type="radio" name="method" id="maxentropy" value="maxentropy">Maximum Entropy</input>
            <input type="radio" name="method" id="svm" value="svm">Support Vector Machine</input>
        </div>
        </form>       
        <div id="results">            
'''
        if(time == 'today'):
            html += '<div id="result-chart"></div>'
        elif(time == 'lastweek'):
            html += '<div id="result-big-chart"></div>'
            
        html += '<div id="content">'
        left = '<div id="left"><h3>Positive</h3><ul>'
        right = '<div id="right"><h3>Negative</h3><ul>'
        middle = '<div id="middle"><h3>Neutral</h3><ul>'
        for i in results:
            res= results[i]
            for j in res:
                item = res[j]
                if(item['label'] == 'positive'):
                    left += '<li title="'+self.weekDates[i]+'">' + item['tweet'] + '</li>'
                elif(item['label'] == 'neutral'):
                    middle+= '<li title="'+self.weekDates[i]+'">' + item['tweet'] + '</li>'
                elif(item['label'] == 'negative'):
                    right += '<li title="'+self.weekDates[i]+'">' + item['tweet'] + '</li>'
            #end innerloop
        #end outerloop
        left += '</ul></div>'
        right += '</ul></div>'
        middle += '</ul></div>'
        html += left + middle + right + '</div>'
        
        if(time == 'today'):
            html += '''        
            </div>
        </div>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
            google.load("visualization", "1", {packages:["corechart"]});
            google.setOnLoadCallback(drawChart);
            function drawChart() {
                var data = google.visualization.arrayToDataTable([
        '''
            html += "['Sentiment', 'Count'],"
            html += "['Positive',  "+ str(pos_count[0]) + "],"
            html += "['Neutral',  "+ str(neut_count[0]) + "],"
            html += "['Negative',  "+ str(neg_count[0]) + "]"
            html += '''
                ]);
    
                var options = {
                  'title': 'Sentiment Classification',
                  'titleTextStyle': {'fontSize': 15},
                  'hAxis': {'textStyle': {'fontSize': 15}},
                  'vAxis': {'textStyle': {'fontSize': 15}},
                  'legend' : {'position' : 'none'}
                };
        
                var chart = new google.visualization.ColumnChart(document.getElementById('result-chart'));
                chart.draw(data, options);      
            }
            '''
        elif(time == 'lastweek'):
            html += '''        
            </div>
        </div>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
            google.load("visualization", "1", {packages:["corechart"]});
            google.setOnLoadCallback(drawChart);
            function drawChart() {
                var data = google.visualization.arrayToDataTable([
        '''
            html += "['Date', 'Positive', 'Neutral', 'Negative'],"
            l = len(pos_count)
            for i in range(l-1, 0, -1):
                html += "['"+ self.weekDates[i] + "', "+ str(pos_count[i]) + "," \
                            + str(neut_count[i]) + "," + str(neg_count[i]) + "],"
            #last one
            html += "['"+ self.weekDates[0] + "', "+ str(pos_count[0]) + "," \
                            + str(neut_count[0]) + "," + str(neg_count[0]) + "]"            
            html += '''
                ]);
    
                var options = {
                  'title': 'Sentiment Classification',
                  'colors': ['#04B404', '#6E6E6E', '#FF0000'],
                  'titleTextStyle': {'fontSize': 15},                  
                  'vAxis': {'textStyle': {'fontSize': 15}},
                  'hAxis': {'textStyle': {'fontSize': 15}, 'slantedText': true, 'slantedTextAngle': 30}
                };
        
                var chart = new google.visualization.LineChart(document.getElementById('result-big-chart'));
                chart.draw(data, options);      
            }
            '''

        checked1 = 'document.getElementById("'+checked+'").checked=true;'
        checked2 = 'document.getElementById("'+time+'").checked=true;'
        textValue = 'document.getElementById("keyword").value="'+keyword+'";'
        html += checked1 + checked2 + textValue
        html += '''        
        function checkEmpty(f) {
            if (f.keyword.value === "") {
                alert('Please enter a valid keyword');
                return false;
            }else{
                f.submit();
                return true;
            }
        }
        var _gaq = _gaq || [];
        _gaq.push(['_setAccount', 'UA-31119754-1']);
        _gaq.push(['_trackPageview']);
        
        (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
        })();   
    </script>
</body>
</html>
'''
        return html
    #end
#end class    
