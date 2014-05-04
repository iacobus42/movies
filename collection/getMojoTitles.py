# -*- coding: utf-8 -*-
"""
Script largely based on the boxofficemojo_parse.py script written and published
by mrphilroth. The orginal script can be found at 
https://github.com/mrphilroth/website-movieratings
"""

import urllib2
from bs4 import BeautifulSoup
import MySQLdb as mdb

# set up the connection to the mysql database movies
con = mdb.connect('localhost', 'simmerin', 'simmerin', 'movies')

# set up a table called mojo, if it already exists, we want to drop it 
# we want to keep title (up to 100 characters), the box office gross, the 
# release month and day. The types are self-explanatory. 
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS mojo")
    cur.execute("CREATE TABLE mojo(id INT PRIMARY KEY AUTO_INCREMENT, \
    title VARCHAR(100), \
    gross INT, \
    month INT, \
    day INT, \
    year INT)")

# Attributes that will identify the table of movie names
tattrs = {'border':'0', 'cellspacing':'1',
          'cellpadding':'5', 'bgcolor':'#ffffff'}

baseurl = ("http://www.boxofficemojo.com/yearly/chart/" +
           "?view=releasedate&view2=domestic&p=.htm")

# Gather the top 300 grossing movies from 1998 to 2014 (range() returns n-1
# as the upper bound, so 2015 is used)
for year in range(1998, 2015):
    for page in [1, 2, 3]:
        # Read the site data
        url = "{}&yr={}&page={}".format(baseurl, year, page)
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        # Identify the table of movie names
        table = soup.find("table", attrs=tattrs)
        # loop through each row and pull out the title, gross and date
        rows = table.find_all("tr")
        nrow = len(rows)
        for i in range(2, (nrow - 4)):
            rowText = rows[i].find_all(text = True)
            rank = rowText[0].replace(",", " ")
            title = rowText[1].replace(",", " ")
            title = title.replace('"', "")
            boxOffice = rowText[3].replace(",", "")
            boxOffice = boxOffice.replace("$", "")
            openingDate = rowText[7].split("/")
            if (title == "Waiting for "):
                title = "Waiting for Superman"
                boxOffice = 6417135
                openingDate = [9, 24]
            try:
                month = openingDate[0]
            except:
                month = "NULL"
            try:
                day = openingDate[1]
            except:
                day = "NULL"
            # inserting into the mojo table
            with con:
                cur.execute("INSERT INTO mojo (title, gross, month, day, year) \
                            VALUES('" + 
                            str(title).replace("'", "") + "', " +
                            str(boxOffice) + ", " +
                            str(month) + ", " + 
                            str(day) + "," + 
                            str(year) + ")")
