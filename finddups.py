#!/usr/bin/python

from __future__ import print_function
import sys
import os
import getopt
import hashlib

filenames_by_size = {}

def md5(fn):
    hash_md5 = hashlib.md5()
    with open(fn, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

filecount = 0

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
            filecount += 1
            if filecount % 100 == 0:
                print("sized " + str(filecount) + " files...",end='\r')

print(" ")

filenames_by_size_copy = {}
for key in filenames_by_size:
    if len(filenames_by_size[key]) > 1:
        filenames_by_size_copy[key] = filenames_by_size[key]

print(str(len(filenames_by_size_copy)) + " suspected dups!")

filecount = 0
filenames_by_hash = {}

for key in filenames_by_size_copy:
    if len(filenames_by_size_copy[key]) > 1:
        for f in filenames_by_size_copy[key]:
            h = md5(f)
            if h not in filenames_by_hash:
                filenames_by_hash[h] = []
            filenames_by_hash[h].append(f)
            filecount += 1
            if filecount % 100 == 0:
                print("hashed " + str(filecount) + " files...",end='\r')

print(" ")
           
for key in filenames_by_hash:
    if len(filenames_by_hash[key]) > 1:
        print("---" + key + "---------------")
        for f in filenames_by_hash[key]:
            print(f)
