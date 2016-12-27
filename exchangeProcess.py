#!/usr/bin/python
# This is a python script to read the output.log and use Blender API to give the data to Blender

import os, sys, time, re

file = open('output.log', 'r')
while True:
    firstLine = file.readline()
    secondLine = file.readline()
    firstLineSuccess = False
    secondLineSuccess = False
    
    r1 = re.compile('Tracker Tracker0@localhost, sensor .*:')
    if r1.match(firstLine) is not None:
        t1 = re.findall('\d+', firstLine) ##ZHA take the second number
        firstLineSuccess = True
    
    secondLine = re.sub('[\s+]', '', secondLine)
    r2 = re.compile('pos(.*,.*,.*);quat(.*,.*,.*,.*)')
    if r2.match(secondLine) is not None:
        t2 = re.findall(r"[-+]?\d*\.\d+|\d+", secondLine) ##ZHA all the elements
        secondLineSuccess = True

    if firstLineSuccess == True and secondLineSuccess == True:
        sensor = int(t1[1])
        x = float(t2[0])
        y = float(t2[1])
        z = float(t2[2])
        rot1 = float(t2[3])
        rot2 = float(t2[4])
        rot3 = float(t2[5])
        rot4 = float(t2[6]);
        
    
    