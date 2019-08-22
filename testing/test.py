#!/usr/bin/python3


import time

from jk_dirmonitor import *





m = DirectoryMonitor("/tmp")

while True:

	newFiles, modifiedFiles, unmodifiedFiles, deletedFiles = m.update()

	print("----------------------------------------------------------------")
	for f in newFiles:
		print("new:", f)
	for f in modifiedFiles:
		print("modified:", f)
	#for f in unmodifiedFiles:
	#	print("unmodified:", f)
	for f in deletedFiles:
		print("deleted:", f)
	print()

	# for demonstation purposes: add additional data
	for f in newFiles:
		f.myAdditionalValue = "abc"

	time.sleep(5)




