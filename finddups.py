#!/usr/bin/python

from __future__ import print_function
import sys
import os
import getopt
import hashlib

filenames_by_size = {}
sizes_by_filename = {}

def md5(fn):
    hash_md5 = hashlib.md5()
    with open(fn, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

filecount = 0
dupcount = 0

for a in sys.argv:
     for dirName, subdirList, fileList in os.walk(a):
        if '.AppleDouble' in dirName:
            continue
        if '@SynoEAStream' in dirName:
            continue
        if '@SynoResource' in dirName:
            continue
        for f in fileList:
            fullpath = os.path.join(dirName,f)
            s = os.path.getsize(fullpath)
            if not s:
                continue
            if s not in filenames_by_size:
                filenames_by_size[s] = []
            filenames_by_size[s].append(fullpath)
            sizes_by_filename[fullpath] = s
            filecount += 1
            if filecount % 100 == 0:
                print("sized " + str(filecount) + " files...",end='\r')
            if len(filenames_by_size[s]) > 1:
                dupcount += 1

print(" ")

print(str(dupcount) + " suspected dups!")

filecount = 0
filenames_by_hash = {}

for key in filenames_by_size:
    if len(filenames_by_size[key]) > 1:
        for f in filenames_by_size[key]:
            h = md5(f)
            if h not in filenames_by_hash:
                filenames_by_hash[h] = []
            filenames_by_hash[h].append(f)
            filecount += 1
            if filecount % 100 == 0:
                print("hashed " + str(filecount) + " files...",end='\r')

print(" ")
           
for k in sorted(filenames_by_hash.keys(), key=lambda x: sizes_by_filename[filenames_by_hash[x][0]], reverse=True):
    print("---" + os.path.basename(filenames_by_hash[k][0]) + "---------------")
    for f in filenames_by_hash[k]:
        print(f)
