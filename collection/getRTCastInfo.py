# -*- coding: utf-8 -*-

import codecs
import time
from rottentomatoes import RT

idfn = "../data/rottenTomatoIds.csv"
ofn = "../data/castData.csv"
ofile = codecs.open(ofn, "w", "utf-8", "replace")
ofile.write("rtID, name, id\n")

movies = open(idfn)
j = 0
keyIndex = 0
keys = ["8frfe3crznr589ddz8m484c9",
        "uhaar3a93r8jqamjzmg5kum8",
        "m5xwmcz54ymb3p7pfnem4nxu"]
currentKey = keys[0]
for line in movies:
    print j, float(j) / 50
    line = line.split(",")
    j = j + 1
    if (line[0] != "year") & (line[3] == "True"): 
        try:
            startTime = time.time()
            rtID = line[4].replace("\n", "")
            cast = RT(currentKey).info(rtID, 'cast')['cast']       
            for actor in cast:
                name = actor['name']
                aid = actor['id']
                ofile.write(u'"{}",{},{}\n'.format(rtID, name, aid))
            endTime = time.time()
            if (endTime - startTime) <= 0.25:
                sleepTime = 0.25 - (endTime - startTime)
                time.sleep(sleepTime)
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
            rtID = line[4].replace("\n", "")
            cast = RT(currentKey).info(rtID, 'cast')['cast']       
            for actor in cast:
                name = actor['name']
                aid = actor['id']
                ofile.write(u'"{}",{},{}\n'.format(rtID, name, aid))
                endTime = time.time()
                if (endTime - startTime) <= 0.25:
                    sleepTime = 0.25 - (endTime - startTime)
                    time.sleep(sleepTime)
ofile.close()    
