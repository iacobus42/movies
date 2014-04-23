# -*- coding: utf-8 -*-

import codecs
import time
from rottentomatoes import RT
rt = RT()

idfn = "../data/rottenTomatoIds.csv"
ofn = "../data/castData.csv"
ofile = codecs.open(ofn, "w", "utf-8", "replace")
ofile.write("rtID, name, id\n")

movies = open(idfn)
j = 0
for line in movies:
    print j, float(j) / 50
    line = line.split(",")
    j = j + 1
    if (line[0] != "year") & (line[3] == "True"): 
        try:
            startTime = time.time()
            rtID = line[4].replace("\n", "")
            cast = rt.info(rtID, 'cast')['cast']       
            for actor in cast:
                name = actor['name']
                aid = actor['id']
                ofile.write(u'"{}",{},{}\n'.format(rtID, name, aid))
            endTime = time.time()
            if (endTime - startTime) <= 0.25:
                sleepTime = 0.25 - (endTime - startTime)
                time.sleep(sleepTime)
        except:
            print "rate limited, waiting 12 hours"
            time.sleep(12 * 60 * 60)
            startTime = time.time()
            rtID = line[4].replace("\n", "")
            cast = rt.info(rtID, 'cast')['cast']       
            for actor in cast:
                name = actor['name']
                aid = actor['id']
                ofile.write(u'"{}",{},{}\n'.format(rtID, name, aid))
                endTime = time.time()
                if (endTime - startTime) <= 0.25:
                    sleepTime = 0.25 - (endTime - startTime)
                    time.sleep(sleepTime)
ofile.close()    
