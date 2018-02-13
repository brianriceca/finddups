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
 	for root, dirs, files in os.walk(a):
		for f in files:
			fullpath = os.path.join(root,f)
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

suspected_dups = 0
for key in filenames_by_size:
	if len(filenames_by_size[key]) > 1:
		suspected_dups += 1

print(str(suspected_dups) + " suspected dups!")

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
		   
for key in filenames_by_hash:
	if len(filenames_by_hash[key]) > 1:
		print("---" + key + "---------------")
		for f in filenames_by_hash[key]:
			print(f)
