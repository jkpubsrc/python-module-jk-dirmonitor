


import os
from typing import Tuple, List

from .FileEntry import FileEntry





class DirectoryMonitor(object):

	def __init__(self, dirPath:str):
		assert isinstance(dirPath, str)
		self.__dirPath = dirPath
		self.__entries = {}									# stores FileEntry objects
	#

	@property
	def dirPath(self) -> str:
		return self.__dirPath
	#

	def get(self, fileName:str) -> FileEntry:
		return self.__entries.get(fileName)
	#

	#
	# Returns a sorted list of file names.
	#
	# @return	str[]		The current set of file names in the directory watched.
	#
	@property
	def fileNames(self) -> list:
		return sorted(self.__entries.keys())
	#

	#
	# Returns a sorted list of file entry objects.
	#
	# @return	FileEntry[]		The current set of file entries in the directory watched.
	#
	@property
	def fileEntries(self) -> list:
		return [ self.__entries[fe] for fe in sorted(self.__entries.keys()) ]
	#

	def update(self) -> Tuple[List, List, List, List]:
		newFiles = []										# stores FileEntry objects
		modifiedFiles = []									# stores FileEntry objects
		unmodifiedFiles = []								# stores FileEntry objects
		namesOfDeletedFiles = set(self.__entries.keys())	# stores string objects

		for dirEntry in os.scandir(self.__dirPath):
			if dirEntry.is_file():
				existingFE = self.__entries.get(dirEntry.name)
				if existingFE is not None:
					# we've seen this file before
					fileEntry = self.__entries[dirEntry.name]
					namesOfDeletedFiles.remove(dirEntry.name)
					stat = dirEntry.stat()
					if (stat.st_mtime > fileEntry._timeStamp) or (stat.st_size != fileEntry._size):
						# file modification time stamp has changed
						fileEntry._timeStamp = stat.st_mtime
						fileEntry._size = stat.st_size
						modifiedFiles.append(fileEntry)
					else:
						# file seems to be unchanged
						unmodifiedFiles.append(fileEntry)
				else:
					# this file is new
					stat = dirEntry.stat()
					fe = FileEntry(dirEntry.name, os.path.abspath(dirEntry.path), stat.st_mtime, stat.st_size)
					self.__entries[fe._name] = fe
					newFiles.append(fe)

		deletedFiles = []									# stores FileEntry objects
		for fileName in namesOfDeletedFiles:
			fe = self.__entries[fileName]
			deletedFiles.append(fe)
			del self.__entries[fileName]

		return newFiles, modifiedFiles, unmodifiedFiles, deletedFiles
	#

#






