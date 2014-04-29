# -*- coding: utf-8 -*-

import codecs
import time
from rottentomatoes import RT

idfn = "../data/rottenTomatoIds.csv"
mfn = "../data/metaData.csv"
mfile = codecs.open(mfn, "w", "utf-8", "replace")
mfile.write("rtID, criticScore, userScore, studio, director, rating, runTime\n")

gfn = "../data/genreData.csv"
gfile = codecs.open(gfn, "w", "utf-8", "replace")
gfile.write("rtID, genre\n")

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
            info = RT(currentKey).info(rtID)      
            critic = info["ratings"]["critics_score"]
            user = info["ratings"]["audience_score"]
            try: 
                studio = info["studio"]
            except:
                studio = ""
            try:
                firstDirector = info["abridged_directors"][0]["name"]
            except:
                firstDirector = ""
            rating = info["mpaa_rating"]
            runTime = info["runtime"]
            mfile.write(u'"{}",{},{},{},{},{},{}\n'.format(rtID, critic, 
                        user, studio, firstDirector, rating, runTime))
            for genre in info["genres"]:
                gfile.write(u'"{}",{}\n'.format(rtID, genre))
            endTime = time.time()
            if (endTime - startTime) <= 0.25:
                sleepTime = 0.25 - (endTime - startTime)
                time.sleep(sleepTime)
        except:
            print "rate limited"
            if (keyIndex < len(keys)):
                print "updating key"
                print "key " + str(keyIndex + 1)                
                keyIndex = keyIndex + 1
                currentKey = keys[keyIndex]
            else:
                print "gonna wait"
                time.sleep(24 * 60 * 60)
                keyIndex = 0
                currentKey = keys[keyIndex]
            info = RT(currentKey).info(rtID)      
            critic = info["ratings"]["critics_score"]
            user = info["ratings"]["audience_score"]
            try: 
                studio = info["studio"]
            except:
                studio = ""
            try:
                firstDirector = info["abridged_directors"][0]["name"]
            except:
                firstDirector = ""
            rating = info["mpaa_rating"]
            runTime = info["runtime"]
            mfile.write(u'"{}",{},{},{},{},{},{}\n'.format(rtID, critic, 
                        user, studio, firstDirector, rating, runTime))
            for genre in info["genres"]:
                gfile.write(u'"{}",{}\n'.format(rtID, genre))
            endTime = time.time()
            if (endTime - startTime) <= 0.25:
                sleepTime = 0.25 - (endTime - startTime)
                time.sleep(sleepTime)
gfile.close()    
mfile.close()