# -*- coding: utf-8 -*-
"""
Script largely based on the boxofficemojo_parse.py script written and published
by mrphilroth. The orginal script can be found at 
https://github.com/mrphilroth/website-movieratings
"""

import time
import codecs
import urllib2
from bs4 import BeautifulSoup

# Output file of movie titles
ofn = "boxofficemojo_titles.csv"
ofile = codecs.open(ofn, "w", "utf-8", "replace")
ofile.write("year,rank,title,boxOffice\n")

# Attributes that will identify the table of movie names
tattrs = {'border':'0', 'cellspacing':'1',
          'cellpadding':'5', 'bgcolor':'#ffffff'}

baseurl = ("http://www.boxofficemojo.com/yearly/chart/" +
           "?view=releasedate&view2=domestic&p=.htm")

# Gather the top 300 grossing movies from the last 15 years
for year in range(1998, 2015) :
    for page in [1, 2, 3] :
        # Read the site data
        url = "{}&yr={}&page={}".format(baseurl, year, page)
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        # Identify the table of movie names
        table = soup.find("table", attrs=tattrs)
        if len(table) != 1 :
            print "Unexpected number of tables on {} page {}".format(year, page)
            continue    
        # Write each movie to the output csv file
        rows = table.find_all("tr")
        nrow = len(rows)
        for i in range(2, (nrow - 4)) :
            rowText = rows[i].find_all(text = True)
            rank = rowText[0].replace(",", " ")
            title = rowText[1].replace(",", " ")
            boxOffice = rowText[3].replace(",", "")
            boxOffice = boxOffice.replace("$", "")
            ofile.write(u'"{}",{},{},{}\n'.format(year, rank, title, boxOffice))

        # Be kind to the boxofficemojo.com domain
        time.sleep(2)

ofile.close()
