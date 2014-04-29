# -*- coding: utf-8 -*-

import codecs
import urllib2
import time
import json
import math
from rottentomatoes import RT

idfn = "../data/rottenTomatoIds.csv"
rfn = "../data/reviewData.csv"
rfile = codecs.open(rfn, "w", "utf-8", "replace")
rfile.write("rtID, reviewer, pub, score, date,fresh\n")

movies = open(idfn)
j = 0
keyIndex = 0
keys = ["8frfe3crznr589ddz8m484c9",
        "uhaar3a93r8jqamjzmg5kum8",
        "m5xwmcz54ymb3p7pfnem4nxu"]
currentKey = keys[0]
for line in movies:
    print j, float(j) / 50
    line = line.split(",")
    j = j + 1
    if j >= 3:
        break
    if (line[0] != "year") & (line[3] == "True"): 
        try:
            startTime = time.time()
            id = line[4].replace("\n", "")
            url = ("http://api.rottentomatoes.com/api/public/v1.0/movies/" + 
                    str(id) + "/reviews.json?review_type=all&page_limit=50" +
                    "&page=1&country=us&apikey=" + str(currentKey))
            reviews = urllib2.urlopen(url)
            reviews = json.load(reviews)  
            totalReviews = reviews["total"]
            totalPages = int(math.ceil(float(totalReviews) / 50))
            for page in range(totalPages):
                if (page != 0):
                    url = ("http://api.rottentomatoes.com/api/public/v1.0/movies/" + 
                            str(id) + "/reviews.json?review_type=all&page_limit=50" +
                               "&page=" + str(page + 1) + 
                               "&country=us&apikey=" + str(currentKey))
                    reviews = json.load(urllib2.urlopen(url))
                reviews = reviews["reviews"]
                for review in reviews:
                    publication = review["publication"].replace(",", " ")
                    criticName = review["critic"]
                    try: 
                        score = review["original_score"].split("/")
                        print score
                        score = float(score[0]) / int(score[1]) * 100
                    except:
                        score = "NA"
                    date = review["date"]
                    fresh = review["freshness"]
                    rfile.write(u'"{}",{},{},{},{},{}\n'.format(id, 
                                    criticName, publication, score, 
                                    date,fresh))
                    endTime = time.time()
                if (endTime - startTime) <= 0.25:
                    sleepTime = 0.25 - (endTime - startTime)
                    time.sleep(sleepTime)
        except:
            print "rate limited"
            if (keyIndex < len(keys)):
                print "updating key"
                print "key " + str(keyIndex + 1)                
                keyIndex = keyIndex + 1
                currentKey = keys[keyIndex]
            else:
                print "gonna wait"
                time.sleep(24 * 60 * 60)
                keyIndex = 0
                currentKey = keys[keyIndex]
            startTime = time.time()
            id = line[4].replace("\n", "")
            url = ("http://api.rottentomatoes.com/api/public/v1.0/movies/" + 
                    str(id) + "/reviews.json?review_type=all&page_limit=50" +
                    "&page=1&country=us&apikey=" + str(currentKey))
            reviews = urllib2.urlopen(url)
            reviews = json.load(reviews)  
            totalReviews = reviews["total"]
            totalPages = int(math.ceil(float(totalReviews) / 50))
            for page in range(totalPages):
                if (page != 0):
                    url = ("http://api.rottentomatoes.com/api/public/v1.0/movies/" + 
                            str(id) + "/reviews.json?review_type=all&page_limit=50" +
                               "&page=" + str(page + 1) + 
                               "&country=us&apikey=" + str(currentKey))
                    reviews = json.load(urllib2.urlopen(url))
                reviews = reviews["reviews"]
                for review in reviews:
                    publication = review["publication"].replace(",", " ")
                    criticName = review["critic"]
                    try: 
                        score = review["original_score"].split("/")
                        score = float(score[0]) / score[1] * 100
                    except:
                        score = "NA"
                    date = review["date"]
                    fresh = review["freshness"]
                    rfile.write(u'"{}",{},{},{},{},{}\n'.format(id, 
                                    criticName, publication, score, 
                                    date,fresh))
                    endTime = time.time()
                if (endTime - startTime) <= 0.25:
                    sleepTime = 0.25 - (endTime - startTime)
                    time.sleep(sleepTime)
rfile.close()