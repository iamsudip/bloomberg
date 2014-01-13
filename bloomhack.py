#!/usr/bin/env python

import sys
# Later when more option will be needed we will use option parser
# Like it will be a long process so we can implement daemon mode or
# we can send date as a argument to the script to fetch the articles from that particular date 
# import argparse
from BeautifulSoup import BeautifulSoup
import requests
import datetime
from pymongo import MongoClient

bloomberg = "http://www.bloomberg.com"
htmlclient = {
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5"
    }
flag = 1

# Assuming mongodb server is running at http://127.0.0.1:27017
client = MongoClient()
db = client.database
posts = db.posts

def store_it(date=None, url=None):
    """
    Stores the scraped data from article link to the database.

    :kwarg date: It holds the date to scrap articles
    :kwarg url: It holds the partial url to a particular article

    """
    
    global htmlclient, posts
    response = requests.get(bloomberg+url, headers=htmlclient)
    if response.status_code==200:
        soup = BeautifulSoup(response.text)
        
        # Scraps the article text
        for article in soup.findAll("div", attrs={"class":"entry_content"}):
            article_text = " ".join([ ptag.text for ptag in article.findAll("p") ])
        
        # data is a dictionary which contains scraped data from the article page
        data = { "author": [ author.text for author in soup.findAll("span", attrs={"class":"author"}) ][0][3:],
            "date": date,
            "article": article_text,
            }
        # Inserting the data to the database
        posts.insert(data)
        print "Inserted article: ", soup.title.text
    else:
        # If any error occurs(generally it doesn't occur like if the link was wrong or it was redirecting to 404) it prints below
        print "Http error: ", response.status_code

def scrap(date=None):
    """
    Scraps the archive to fetch all the article links in a given date

    :kwarg date: It holds the date to scrap articles links
    """
    
    global htmlclient, bloomberg
    response = requests.get(bloomberg+"/archive/news/"+date, headers=htmlclient)
    if response.status_code==200:
        soup = BeautifulSoup(response.text)
        
        # Getting the urls to all the posts from the archive at the given date
        for story_list in soup.findAll("ul", attrs={"class":"stories"}):
            storylinks = [ story.a.get("href") for story in story_list.findAll("li") ]
        
        # Function call to store the link contents
        for story in storylinks:
            store_it(date, story)
        return 1
    
    # Set flag to -1 when there is no posts available(i.e. status code is 408) in the archive or
    # it already stored all the articles from bloomberg
    else: 
        return -1

def main():
    """
    The famous main function which mainly controls all the code here :p
    """
    try:
        global flag
        date = datetime.date.today().strftime("%Y-%m-%d")
        while flag is 1:
            flag = scrap(date)
            print "Stored all the articles of: ", date
            date = date - datetime.timedelta(1)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__=='__main__':
    main()

