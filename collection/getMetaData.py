# -*- coding: utf-8 -*-


import time
from rottentomatoes import RT
import MySQLdb as mdb

con = mdb.connect('localhost', 'simmerin', 'simmerin', 'movies')
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS genres")
    cur.execute("CREATE TABLE genres(gepk INT PRIMARY KEY AUTO_INCREMENT, \
    rtid INT, \
    genre VARCHAR(50))")
    cur.execute("DROP TABLE IF EXISTS metadata")
    cur.execute("CREATE TABLE metadata (mpk INT PRIMARY KEY AUTO_INCREMENT,\
    rtid INT, \
    criticScore INT, \
    userScore INT,\
    director VARCHAR(100),\
    studio VARCHAR(50),\
    rating VARCHAR(10),\
    runTime INT)")


j = 0
keyIndex = 0
keys = ["uhaar3a93r8jqamjzmg5kum8",
        "8frfe3crznr589ddz8m484c9",
        "m5xwmcz54ymb3p7pfnem4nxu"]
currentKey = keys[0]
with con:
    cur.execute("SELECT rtid FROM rtid WHERE rtid IS NOT NULL")
    rtids = map(lambda x: x[0], cur.fetchall())
    
for rtID in rtids:
    print j, float(j) / 50
    j = j + 1
    try:
        startTime = time.time()
        info = RT(currentKey).info(rtID)      
        critic = info["ratings"]["critics_score"]
        if (critic == -1):
            critic = "NULL"
        user = info["ratings"]["audience_score"]
        if (user == -1):
            user = "NULL"
        try: 
            studio = info["studio"]
        except:
            studio = "NULL"
        try:
            firstDirector = info["abridged_directors"][0]["name"]
        except:
            firstDirector = "NULL"
        rating = info["mpaa_rating"]
        runTime = info["runtime"]
        try:
            runTime = int(runTime)
        except:
            runTime = "NULL"
        with con:
            cur.execute("INSERT INTO metadata (rtid, criticScore, userScore, \
                     director, studio, rating, runTime) VALUES (" + 
                     str(rtID) + ", " + 
                     str(critic) + ", " + 
                     str(user) + ", '" +
                     str(firstDirector.replace("'", "")) + "', '" + 
                     str(studio.replace("'", "")) + "', '" + 
                     str(rating) + "', " + 
                     str(runTime) + ")")
            for genre in info["genres"]:
                cur.execute("INSERT INTO genres (rtid, genre) VALUES (" +
                             str(rtID) + ", '" + 
                             str(genre) + "')")
        endTime = time.time()
        if (endTime - startTime) <= 0.5:
            sleepTime = 0.5 - (endTime - startTime)
            time.sleep(sleepTime)
    except:
        print "rate limited"
        if (keyIndex < (len(keys) - 1)):
            print "updating key"
            print "key " + str(keyIndex + 1)                
            keyIndex = keyIndex + 1
            currentKey = keys[keyIndex]
        else:
            print "gonna wait"
            time.sleep(20 * 60)
            keyIndex = 0
            currentKey = keys[keyIndex]
        startTime = time.time()
        info = RT(currentKey).info(rtID)      
        critic = info["ratings"]["critics_score"]
        if (critic == -1):
            critic = "NULL"
        user = info["ratings"]["audience_score"]
        if (user == -1):
            user = "NULL"
        try: 
            studio = info["studio"]
        except:
            studio = "NULL"
        try:
            firstDirector = info["abridged_directors"][0]["name"]
        except:
            firstDirector = "NULL"
        rating = info["mpaa_rating"]
        runTime = info["runtime"]
        try:
            runTime = int(runTime)
        except:
            runTime = "NULL"
        with con:
            cur.execute("INSERT INTO metadata VALUES (" + 
                     str(rtID) + ", " + 
                     str(critic) + ", " + 
                     str(user) + ", '" +
                     str(firstDirector.replace("'", "")) + "', '" + 
                     str(studio.replace("'", "")) + "', '" + 
                     str(rating) + "', " + 
                     str(runTime) + ")")
            for genre in info["genres"]:
                 cur.execute("INSERT INTO genres (rtid, genre) VALUES (" +
                             str(rtID) + ", '" + 
                             str(genre) + "')")
        endTime = time.time()
        if (endTime - startTime) <= 0.5:
            sleepTime = 0.5 - (endTime - startTime)
            time.sleep(sleepTime)