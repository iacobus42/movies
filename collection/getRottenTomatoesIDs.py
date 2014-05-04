# -*- coding: utf-8 -*-

import time
from rottentomatoes import RT
rt = RT("uhaar3a93r8jqamjzmg5kum8")
import MySQLdb as mbd

# set up the connection to the MySQL database
con = mbd.connect('localhost', 'simmerin', 'simmerin', 'movies')

j = 0 # a counter for debugging purposes
with con:
    cur = con.cursor()
    # drop the table if it exists to prevent adding movies multiple times
    cur.execute("DROP TABLE IF EXISTS rtid")
    # create the table as detailed in the documentation
    cur.execute("CREATE TABLE rtid(id INT PRIMARY KEY AUTO_INCREMENT, \
                 rtid INT)")
    # bring in the titles and years from the Box Office Mojo data
    cur.execute("SELECT * FROM mojo")
    titles = cur.fetchall()
    # loop through each title and pull out the rt id for the first film
    # returned from the RT search with the correct year, if no matches
    # use NULL for the rt id
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
        # rt api limits to 5 calls per second, with latency this turns out to 
        # be more like 4 calls per second. Space out the calls by at least
        # 0.25 seconds
        if (endTime - startTime) < 0.25:
            time.sleep(0.25 - (endTime - startTime))


