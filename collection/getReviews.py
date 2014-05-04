# -*- coding: utf-8 -*-

import urllib2
import json
import math
import time
import MySQLdb as mbd
               
con = mbd.connect('localhost', 'simmerin', 'simmerin', 'movies')

with con:
    # set up the connection and the tables
    cur = con.cursor()
    # the following line is commented out "for safety" as this program takes
    # >= 6 hours to run and I do not want to accidentally drop the table!
    # When running for the first time the following lines should be uncommented
    #cur.execute("DROP TABLE IF EXISTS reviews")
    #cur.execute("CREATE TABLE reviews (\
    #                 reviewID INT PRIMARY KEY AUTO_INCREMENT, \
    #                 rtid INT, \
    #                 reviewer VARCHAR(50), \
    #                 publication VARCHAR(100), \
    #                 month INT, \
    #                 year INT, \
    #                 score INT, \
    #                 fresh INT)")
                
    cur.execute("SELECT rtid FROM rtid WHERE rtid IS NOT NULL")
    
rtids = map(lambda x: x[0], cur.fetchall())
j = -1 # counter as before
keyIndex = 0 # key handling logic is the same as the other scripts
keys = ["gkruk3vzfg2vqbv76t94dy5r",
        "39jxydympemjqq5g228achpp"]
currentKey = keys[keyIndex]
# loop through each id and grab the reviews
for id in rtids:
    j = j + 1          
    try:
        startTime = time.time()
        # call out to the api
        url = ("http://api.rottentomatoes.com/api/public/v1.0/movies/" + 
                str(id) + "/reviews.json?review_type=all&page_limit=50" +
                "&page=1&country=us&apikey=" + str(currentKey))
        reviews = urllib2.urlopen(url)
        # parse the json
        reviews = json.load(reviews)  
        totalReviews = reviews["total"]
        # I can only return 50 reviews per page, so find the total 
        # number of pages required to show all the reviews
        totalPages = int(math.ceil(float(totalReviews) / 50))
        # loop through all of the pages required
        for page in range(totalPages):
            # we already made the first call, so no need to repeat it
            if (page != 0):
                startTime = time.time()
                url = ("http://api.rottentomatoes.com/api/public/v1.0/movies/" + 
                        str(id) + "/reviews.json?review_type=all&page_limit=50" +
                        "&page=" + str(page + 1) + 
                        "&country=us&apikey=" + str(currentKey))
                reviews = json.load(urllib2.urlopen(url))
            reviews = reviews["reviews"]
            # loop through the reviews in each page and pull out the score,
            # month, year, reviewer, etc
            for review in reviews:
                pub = review["publication"].replace(",", " ").replace("'", "")
                reviewerName  = review["critic"].replace("'", "")
                try: 
                    score = review["original_score"].split("/")
                    score = int(round(float(score[0]) / int(score[1]) * 100))
                except:
                    score = "NULL"
                try:
                    date = review["date"].split("-")
                    try:
                        month = date[1]
                    except:
                        month = "NULL"
                    try:
                        year = date[0]
                    except:
                        year = "NULL"
                except:
                    month = "NULL"
                    year = "NULL"
                    
                fresh = int((review["freshness"] == "fresh") * 1)
                with con:
                    # write to the database
                    cur.execute("INSERT INTO reviews (rtid, reviewer, publication, month, year, score, fresh) \
                            VALUES (" + str(id) + ", '" +
                            str(reviewerName) + "', '" + 
                            str(pub) + "', " + 
                            str(month) + ", " + 
                            str(year) + ", " + 
                            str(score) + ", " + 
                            str(fresh) + ")")
                endTime = time.time()
                # sleep if required to stay under the rate limit
                if (endTime - startTime) <= 0.275:
                    sleepTime = 0.275 - (endTime - startTime)
                    time.sleep(sleepTime)
    except:
        # same rate limit handling logic as in the other scripts
        print "rate limited"
        if (keyIndex < 2):
            print "updating key"
            print "key " + str(keyIndex + 1)                
            keyIndex = keyIndex + 1
            currentKey = keys[keyIndex]
            time.sleep(0.25)
        else:
            print "gonna wait"
            time.sleep(20 * 60)
            keyIndex = 0
            currentKey = keys[keyIndex]
        startTime = time.time()
        reviews = urllib2.urlopen(url)
        reviews = json.load(reviews)  
        totalReviews = reviews["total"]
        totalPages = int(math.ceil(float(totalReviews) / 50))
        for page in range(totalPages):
            if (page != 0):
                startTime = time.time()
                url = ("http://api.rottentomatoes.com/api/public/v1.0/movies/" + 
                        str(id) + "/reviews.json?review_type=all&page_limit=50" +
                        "&page=" + str(page + 1) + 
                        "&country=us&apikey=" + str(currentKey))
                reviews = json.load(urllib2.urlopen(url))
            reviews = reviews["reviews"]
            for review in reviews:
                pub = review["publication"].replace(",", " ").replace("'", "")
                reviewerName  = review["critic"].replace("'", "")
                try: 
                    score = review["original_score"].split("/")
                    score = int(round(float(score[0]) / int(score[1]) * 100))
                except:
                    score = "NULL"
                try:
                    date = review["date"].split("-")
                    try:
                        month = date[1]
                    except:
                        month = "NULL"
                    try:
                        year = date[0]
                    except:
                        year = "NULL"
                except:
                    month = "NULL"
                    year = "NULL"
                    
                fresh = int((review["freshness"] == "fresh") * 1)
                endTime = time.time()
                with con:                
                    cur.execute("INSERT INTO reviews (rtid, reviewer, publication, month, year, score, fresh) \
                            VALUES (" + str(id) + ", '" + 
                            str(reviewerName) + "', '" + 
                            str(pub) + "', " + 
                            str(month) + ", " + 
                            str(year) + ", " + 
                            str(score) + ", " + 
                            str(fresh) + ")")
                if (endTime - startTime) <= 0.275:
                    sleepTime = 0.275 - (endTime - startTime)
                    time.sleep(sleepTime)
        
        
