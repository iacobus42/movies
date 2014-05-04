# -*- coding: utf-8 -*-

import time
from rottentomatoes import RT
rt = RT("uhaar3a93r8jqamjzmg5kum8")
import MySQLdb as mbd

# set up connection to MySQL database
con = mbd.connect('localhost', 'simmerin', 'simmerin', 'movies')

with con:
    cur = con.cursor()
    # as before, create the table
    cur.execute("DROP TABLE IF EXISTS cast")
    cur.execute("CREATE TABLE cast (castpk INT PRIMARY KEY AUTO_INCREMENT, \
                 actorID INT, \
                 actorName VARCHAR(50), \
                 rtid INT)")
    cur.execute("SELECT rtid FROM rtid WHERE rtid IS NOT NULL")
    # the fetchall() for the query returns a list of tuples, each tuple
    # of length 1 containing the rtid. We need to make this into a 
    # list of the rtids, not in tuples. The fastest and cleanest way
    # is to use the functional map() with an anonoymous function to
    # extract the first element. This is used whenever I need the rtids. 
    rtids = map(lambda x: x[0], cur.fetchall())
    j = 0 # a counter for debugging
    # by default, rt places a limit of 10,000 queries per day. This can
    # be increased by contacting support with a request. However, for this
    # project, it was simpler to just apply for multiple keys. The try/except
    # block below deals with rate limiting and changes the key as needed. 
    # keyIndex is the index of the current key in the list keys. 
    keyIndex = 0 
    keys = ["8frfe3crznr589ddz8m484c9",
            "uhaar3a93r8jqamjzmg5kum8",
            "m5xwmcz54ymb3p7pfnem4nxu"]
    currentKey = keys[0]
    # loop through the rtids and for each rtid make an API call to get the 
    # cast information from RT. This comes back as a JSON.
    for rtid in rtids:
        print j
        try:
            startTime = time.time()
            cast = RT(currentKey).info(rtid, 'cast')['cast'] 
            # loop through each element in the `cast` element of the JSON
            # results and pull out the name, id and rtid.       
            for actor in cast:
                name = actor['name'].replace("'", "")
                aid = actor['id']
                cur.execute("INSERT INTO cast (actorID, actorName, rtid) \
                             VALUES(" + 
                             str(aid) + ", '" + 
                             str(name) + "', " +
                             str(rtid) + ")")
            endTime = time.time()
            # sleep, as needed, to avoid rate limiting
            if (endTime - startTime) <= 0.25:
                sleepTime = 0.25 - (endTime - startTime)
                time.sleep(sleepTime)
            j = j + 1
        except:
            # logic to handle http 403 (rate limit) errors. Either
            # increase the keyIndex value by 1 (move to the next key)
            # or sleep for 24 hours (exhausted all the keys). After
            # either step, rerun the above code with the fresh keys. 
            print "rate limited"
            if (keyIndex < 2):
                print "updating key"
                print "key " + str(keyIndex)                
                keyIndex = keyIndex + 1
                currentKey = keys[keyIndex]
            else:
                print "gonna wait"
                time.sleep(24 * 60 * 60)
                keyIndex = 0
                currentKey = keys[keyIndex]
            startTime = time.time()
            cast = RT(currentKey).info(rtid, 'cast')['cast']       
            for actor in cast:
                name = actor['name']
                aid = actor['id']
                cur.execute("INSERT INTO cast (actorID, actorName, rtid) \
                             VALUES(" + 
                             str(aid) + ", '" + 
                             str(name) + "', " +
                             str(rtid) + ")")
            endTime = time.time()
            if (endTime - startTime) <= 0.25:
                sleepTime = 0.25 - (endTime - startTime)
                time.sleep(sleepTime)
            j = j + 1