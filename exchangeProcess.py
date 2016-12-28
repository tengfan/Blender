#!/usr/bin/python
# This is a python script to read the output.log and use Blender API to give the data to Blender

import io, os, sys, time, re, subprocess, threading
import queue
import bpy

global q
q = queue.Queue()
qT1 = queue.Queue()
qT2 = queue.Queue()

def executeExe():
    print("executeExe launched")
    global file
    file = io.StringIO()
    cmd = "vrpn_print_devices.exe Tracker0@localhost"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline, ''):
        line = str(line, "utf-8")
        q.put(line)

def treatment():
    print("treatment launched")  

    while True:
        firstLineSuccess = False
        secondLineSuccess = False
        
        if not q.empty():
            firstLine = q.get()
            r1 = re.compile('Tracker Tracker0@localhost, sensor .*:')
            if r1.match(firstLine) is not None:
                t1 = re.findall('\d+', firstLine) ##ZHA take the second number
                firstLineSuccess = True
                #print(t1)
                qT1.put(t1)

        if not q.empty():
            secondLine = q.get()
            secondLine = re.sub('[\s+]', '', secondLine)
            r2 = re.compile('pos(.*,.*,.*);quat(.*,.*,.*,.*)')
            if r2.match(secondLine) is not None:
                t2 = re.findall(r"[-+]?\d*\.\d+|\d+", secondLine) ##ZHA all the elements
                secondLineSuccess = True
                #print(t2)
                qT2.put(t2)

def sendToBlender():
    t1 = ['0','0']
    t2 = ['0','0','0','0','0']
    i = 0
    while True:
        if not qT1.empty():
            t1 = qT1.get()
        if not qT2.empty():
            t2 = qT2.get()
        i+=1
        if i == 97:
            i = 0
            
        if i == 1:
            sensor = int(t1[1])
            x = float(t2[0])
            y = float(t2[1])
            z = float(t2[2])
            rot1 = float(t2[3])
            rot2 = float(t2[4])
            rot3 = float(t2[5])
            rot4 = float(t2[6])
            bpy.data.meshes["sens'"+sensor+":x"] = x
            bpy.data.meshes["sens'"+sensor+":y"] = y
            bpy.data.meshes["sens'"+sensor+":z"] = z
            bpy.data.meshes["sens'"+sensor+":rot1"] = rot1
            bpy.data.meshes["sens'"+sensor+":rot2"] = rot2
            bpy.data.meshes["sens'"+sensor+":rot3"] = rot3
            bpy.data.meshes["sens'"+sensor+":rot4"] = rot4;
        

thread1 = threading.Thread(target=executeExe, args=[])
thread2 = threading.Thread(target=treatment, args=[])
thread3 = threading.Thread(target=sendToBlender, args=[])

thread1.start()
time.sleep(0.2)
thread2.start()
time.sleep(0.2)
thread3.start()