# -*- coding: utf-8 -*-

import time
from rottentomatoes import RT
rt = RT("uhaar3a93r8jqamjzmg5kum8")
import MySQLdb as mbd

con = mbd.connect('localhost', 'simmerin', 'simmerin', 'movies')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS cast")
    cur.execute("CREATE TABLE cast (castpk INT PRIMARY KEY AUTO_INCREMENT, \
                 actorID INT, \
                 actorName VARCHAR(50), \
                 rtid INT)")
    cur.execute("SELECT rtid FROM rtid WHERE rtid IS NOT NULL")
    rtids = map(lambda x: x[0], cur.fetchall())
    j = 0
    keyIndex = 0
    keys = ["8frfe3crznr589ddz8m484c9",
            "uhaar3a93r8jqamjzmg5kum8",
            "m5xwmcz54ymb3p7pfnem4nxu"]
    currentKey = keys[0]
    for rtid in rtids:
        print j
        try:
            startTime = time.time()
            cast = RT(currentKey).info(rtid, 'cast')['cast']       
            for actor in cast:
                name = actor['name'].replace("'", "")
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
        except:
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