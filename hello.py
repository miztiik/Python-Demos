#!/usr/bin/python
# -*- coding: utf-8 -*-

# import boto3
# 
# 
# ec2 = boto3.resource('ec2')
# vpc = ec2.Vpc('id')
# 
# 
# yum -y install epel-release
# yum -y install python-pip unzip
# pip install --upgrade pip
# pip install requests unidecode flask flask-ask
# cd /tmp;curl -O https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip


import feedparser, json, time , traceback

from datetime import datetime
from flask import Flask
from flask import request


app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to my world"



if __name__ == "__main__":
    app.run()







@app.route("/get_news")
def lambda_handler(event={}, context={}):

    # event['cutoff'] = 60000
    
    rssUrlList = {
            "topstories": { 
                "googlenews"        : "https://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&output=rss"
            },
    
            "india" : {
                "googlenews"        : "http://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&topic=n&output=rss",
                "bbc"               : "http://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
                "hindu"             : "http://www.thehindubusinessline.com/news/national/?service=rss"
            }
    }

    
    """
    Funtion to Iterate dictionary of dictionaries
    @Arg - Takes one arugment of type dictionary
    Checks if the value of a dictionary is a dictionary and call itself
    If NOT dictionary calls the getNews Fuction
    """
    
    def recurseDict(d,pk=None):
        pk = pk
        for k, v in d.items():
            if isinstance(v, dict):
                recurseDict( d[k], k )
            else:
                # print( "\n{0} : {1} : {2}".format(pk,k, v) )
                getNews( pk, k, v )
    
    
    """
    Function to collect data from BBC RSS Feed for india
    Get only the summary for articles which were published today
    """
    def getNews(sectiontitle, mediagroup, url):
    
        newsFeed = {}
        articles = {}
        newsitems = []

        # Set the news cutoff time
        if 'cutoff' in event:
           # 16 Hours ( 16 * 3600)
           # cutOffTime = 57600
           cutOffTime = int(event['cutoff'])
        else:
           cutOffTime = 36000
        
        try:
            feed = feedparser.parse(url)
            if feed:
                for entry in feed['entries']:
    
                    newsTxt = ''
    
                    last_updated = time.mktime( entry['published_parsed'] )
                    currLocalTime = time.mktime(time.localtime())
    
                    publishedTime = str( entry['published_parsed'][3] ) + " hours ago."
                    
                    # pdb.set_trace()
                    # Check if the articles are lesser than a given time period
                    if ( currLocalTime - last_updated )  < cutOffTime:
                        if ( mediagroup == "googlenews" ) or ( mediagroup == "businessinsider" ):
                            newsTxt = entry['title_detail']['value'] 
                        elif ( mediagroup == "economictimes" ):
                            newsTxt = entry['title']
                        else:
                            newsTxt = entry['summary_detail']['value']
                    
                    # Add to newsitems only if our cutoff criteria is met
                    if newsTxt:
                        newsitems.append( newsTxt + " , Reported at around " + publishedTime  )
                
                # Add an polite error message is no matches are found within the cutoff criteria
                if not newsitems:
                    newsitems.append( "Probably nothing worth reporting happened in the past " + str(cutOffTime /3600) + " hours."  )
    
                articles[ 'newsitems' ] = newsitems
                articles[ 'sectiontitle' ] = sectiontitle
                articles[ 'mediagroup' ] = mediagroup
        
        except Exception as e:
            articles[ 'newsitems' ] = "Error : " + traceback.format_exc()
            articles[ 'sectiontitle' ] = sectiontitle
            articles[ 'mediagroup' ] = mediagroup
        
        # Lets collate the news
        collateNews ( articles )
        return    
    
    """
    Merge same section titles together
    """
    def collateNews( newsFeed ):
        #pdb.set_trace()
        # Check if the section title dictionary is already in the collacted news items,
        # If it is there, then add that dictionary to the existing one
    
        tempDict = {}
        tempDict[ newsFeed['mediagroup'] ] = newsFeed[ 'newsitems' ]
    
        if newsFeed['sectiontitle'] in collatedNews:
            # collatedNews[ newsFeed['sectiontitle'] ][  ].update( newsFeed[ 'newsitems' ] )
            collatedNews[ newsFeed['sectiontitle'] ].update( tempDict )
        
        # update the section if it is not there already
        else:
            # collatedNews.update ( newsFeed )
    
            collatedNews[ newsFeed['sectiontitle'] ] = tempDict
    
    # Lets collect some news
    collatedNews = {}
    recurseDict( rssUrlList )
    #recurseDict( rssUrlListTest )
    print collatedNews
    return json.dumps(collatedNews)



