# -*- coding: utf-8 -*-

import time
from rottentomatoes import RT
rt = RT("uhaar3a93r8jqamjzmg5kum8")
import MySQLdb as mbd

con = mbd.connect('localhost', 'simmerin', 'simmerin', 'movies')

j = 0
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS rtid")
    cur.execute("CREATE TABLE rtid(id INT PRIMARY KEY AUTO_INCREMENT, \
                 rtid INT)")
    cur.execute("SELECT * FROM mojo")
    titles = cur.fetchall()
    for movie in titles:
        print j
        title = movie[1]
        year = movie[5]
        startTime = time.time()
        searchResults = rt.search(title)
        correctFilm = 0    
        found = False
        for result in searchResults:
            if result["year"] == year:
                correctFilm = result
                found = True
                break
        if found:
            rtID = correctFilm["id"]
        else:
            rtID = "NULL"
        cur.execute("INSERT INTO rtid (rtid) VALUE (" + str(rtID) + ")")
        j = j + 1
        endTime = time.time()
        if (endTime - startTime) < 0.25:
            time.sleep(0.25 - (endTime - startTime))


