# -*- coding: utf-8 -*-

import codecs
import time
from rottentomatoes import RT
rt = RT()

tfn = "../data/boxofficemojo_titles.csv"
ofn = "../data/rottenTomatoIds.csv"
ofile = codecs.open(ofn, "w", "utf-8", "replace")
ofile.write("mojoTitle, rtTitle, year, found, rtID\n")

titles = open(tfn)
j = 0
for line in titles:
    print j
    line = line.split(",")
    if line[0] != "year": 
        title = line[2]
        year = line[0]
        searchResults = rt.search(title)
        correctFilm = 0    
        found = False
        for result in searchResults:
            if result["year"] == int(year):
                correctFilm = result
                found = True
                break
        if found:
            year = correctFilm["year"]
            rtTitle = correctFilm["title"].replace(",", " ")
            rtID = correctFilm["id"]
            ofile.write(u'"{}",{},{},{},{}\n'.format(title, rtTitle, year, 
                        found, rtID))
        else:
            rtTitle = ""
            rtID = ""
            ofile.write(u'"{}",{},{},{},{}\n'.format(title, rtTitle, year, 
                        found, rtID))
        j = j + 1
        time.sleep(0.25)


ofile.close()    

