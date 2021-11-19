#! /usr/bin/python3

import os
from utils import nasa_parser

asteroidList = open("./utils/asteroids.txt","r")
startLine = 1
endLine = 31

lineCounter = 1

#Startup
# 1. Clean failed log
open('./log/failed-asteroids.txt', 'w').close()
# 2. Clean screenshots directory
dir = './images/screenshots'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

for asteroidName in asteroidList:
    if lineCounter == endLine:
        break
    if startLine <= lineCounter:
        nasa_parser.NASAParser(asteroidName)
    lineCounter += 1
