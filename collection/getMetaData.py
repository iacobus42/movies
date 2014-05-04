# -*- coding: utf-8 -*-


import time
from rottentomatoes import RT
import MySQLdb as mdb

# connect to the movies database
con = mdb.connect('localhost', 'simmerin', 'simmerin', 'movies')
with con:
    cur = con.cursor()
    # create table to hold genre data
    cur.execute("DROP TABLE IF EXISTS genres")
    cur.execute("CREATE TABLE genres(gepk INT PRIMARY KEY AUTO_INCREMENT, \
    rtid INT, \
    genre VARCHAR(50))")
    # create table to hold 1 to 1 metadata
    cur.execute("DROP TABLE IF EXISTS metadata")
    cur.execute("CREATE TABLE metadata (mpk INT PRIMARY KEY AUTO_INCREMENT,\
    rtid INT, \
    criticScore INT, \
    userScore INT,\
    director VARCHAR(100),\
    studio VARCHAR(50),\
    rating VARCHAR(10),\
    runTime INT)")


j = 0 # counter for debugging 
# a list of keys and a index for the current key to deal with rate
# limits imposed by the RT api
keyIndex = 0 
keys = ["uhaar3a93r8jqamjzmg5kum8",
        "8frfe3crznr589ddz8m484c9",
        "m5xwmcz54ymb3p7pfnem4nxu"]
currentKey = keys[0]
with con:
    # as before, we want the rtids and we need to extract them
    # from the list of tuples
    cur.execute("SELECT rtid FROM rtid WHERE rtid IS NOT NULL")
    rtids = map(lambda x: x[0], cur.fetchall())
    
# loop through each rtid and grab the metadata
for rtID in rtids:
    print j
    j = j + 1
    try:
        startTime = time.time()
        info = RT(currentKey).info(rtID)      
        critic = info["ratings"]["critics_score"]
        # if there is no critic score, RT returns -1. We want this value to 
        # be NULL in the database, so deal with it here
        if (critic == -1):
            critic = "NULL"
        user = info["ratings"]["audience_score"]
        # same with user score
        if (user == -1):
            user = "NULL"
        # not all films have a studio in the results and for films without
        # a studio, the JSON results do not contain a studio element, so 
        # use a try/except block to get that data or NULL, as needed
        try: 
            studio = info["studio"]
        except:
            studio = "NULL"
        # same with director. Additionally, some films have >1 directors, 
        # I keep only the first director
        try:
            firstDirector = info["abridged_directors"][0]["name"]
        except:
            firstDirector = "NULL"
        rating = info["mpaa_rating"]
        runTime = info["runtime"]
        # all films have runtime in their results, but some are not valid
        # and are a string of the sort NA. Use int() to sort these out and
        # replace the missing runtimes with null. 
        try:
            runTime = int(runTime)
        except:
            runTime = "NULL"
        with con:
            # add the data to the table
            cur.execute("INSERT INTO metadata (rtid, criticScore, userScore, \
                     director, studio, rating, runTime) VALUES (" + 
                     str(rtID) + ", " + 
                     str(critic) + ", " + 
                     str(user) + ", '" +
                     str(firstDirector.replace("'", "")) + "', '" + 
                     str(studio.replace("'", "")) + "', '" + 
                     str(rating) + "', " + 
                     str(runTime) + ")")
            # loop through each genre listed for the film and insert into the 
            # genres table
            for genre in info["genres"]:
                cur.execute("INSERT INTO genres (rtid, genre) VALUES (" +
                             str(rtID) + ", '" + 
                             str(genre) + "')")
        endTime = time.time()
        # i was getting a lot of latency problems with this script and so 
        # set the interval to 0.5 seconds instead of the 0.25 seconds used
        # in my other scripts
        if (endTime - startTime) <= 0.5:
            sleepTime = 0.5 - (endTime - startTime)
            time.sleep(sleepTime)
    except:
        # same key handling/sleep logic as in getCastInfo.py
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