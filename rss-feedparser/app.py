#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template,redirect, url_for, request
import feedparser,requests,json
import time

from datetime import datetime
import traceback,pdb,os

app = Flask(__name__)

@app.route("/newsSpider", methods = ["GET", "POST"] )
def newsSpider():

    rssUrlList = {
            "topstories": { 
                "googlenews"        : "https://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&output=rss",
                "economictimes"     : "http://economictimes.indiatimes.com/rssfeedstopstories.cms"
            },
    
            "india" : {
                "googlenews"        : "http://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&topic=n&output=rss",
                "bbc"               : "http://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
                "hindu"             : "http://www.thehindubusinessline.com/news/national/?service=rss"
            },
    
            "world" : {
                "googlenews"        : "https://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&topic=w&output=rss",
                "bbc"               : "http://feeds.bbci.co.uk/news/world/rss.xml",
                "hindu"             : "http://www.thehindubusinessline.com/news/national/?service=rss"
            },
    
            "business" : {
                "economictimes"     : "http://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
                "hindu"             : "http://www.thehindubusinessline.com/markets/?service=rss",
                "googlenews"        : "http://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&topic=b&output=rss"
            },
    
            "opinion" : {
                "hindu"             : "http://www.thehindubusinessline.com/opinion/?service=rss",
                "businessinsider"   : "http://www.businessinsider.in/rss_ptag_section_feeds.cms?query=indiainsider"
            }
    }   

    if request.method == "GET":
        error = None
        # Render just the template when method is "GET"
        return render_template ( "newsSpider.html", rssUrlList = rssUrlList  )

    if request.method == "POST":

        event = { "newsSection" : request.form["newsSection"] }
        #event = { "newsSection" : "india" }

        """
        Funtion to Iterate dictionary of dictionaries
        @Arg - Takes one arugment of type dictionary
        Checks if the value of a dictionary is a dictionary and call itself
        If NOT dictionary calls the getNews Fuction
        """
        def recurseDict(d, newsSection=None):
            pk = newsSection
            for k, v in d.items():
                if isinstance(v, dict):
                    # If any preference is given fetch only
                    if k == pk or pk is None:
                        recurseDict( d[k], k )
                else:
                    # print( "\n{0} : {1} : {2}".format(pk, k, v) )
                    getNews( pk, k, v )
    
        """
        Function to collect data from BBC RSS Feed for india
        Get only the summary for articles which were published today
        """
        def getNews(sectiontitle, mediagroup, url):
        
            newsFeed = {}
            articles = {}
            newsitems = []
    
            # Parsing through parameters to shrink or widen news collection
            # Set the news cutoff time
            if 'cutOffTime' in event:
               # 16 Hours ( 16 * 3600)
               # cutOffTime = 57600
               cutOffTime = int(event['cutOffTime'])
            else:
               cutOffTime = 864000
            
            try:
                feed = feedparser.parse(url)
                if feed:
                    for entry in feed['entries']:
        
                        newsTxt = ''
        
                        last_updated = time.mktime( entry['published_parsed'] )
                        currLocalTime = time.mktime(time.localtime())
        
                        publishedTime = str( entry['published_parsed'][3] ) + " hours ago."
                        
                        # Check if the articles are lesser than a given time period
                        if ( currLocalTime - last_updated )  < cutOffTime:
                            if ( mediagroup == "googlenews" ) or ( mediagroup == "businessinsider" ):
                                newsTxt = entry['title_detail']['value'] 
                            elif ( mediagroup == "economictimes" ):
                                newsTxt = entry['title']
                            else:
                                newsTxt = entry['summary_detail']['value']
    
                        if newsTxt:
                            newsitems.append( newsTxt + " , Reported at around " + publishedTime  )
    
                    if not newsitems:
                        newsitems.append( "Pfttt!! Nothing new since the last " + str( cutOffTime / 3600) + " hours."  )
    
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
        
        # Parsing through parameters to shrink or widen news collection
        # Set the news cutoff time
        if 'newsSection' in event:
           recurseDict( rssUrlList, event['newsSection'] )
        else:
            recurseDict( rssUrlList )
        
        return render_template( "newsSpider.html" , rssUrlList = rssUrlList, result = collatedNews )

if __name__ == '__main__':
   app.run( debug = True )