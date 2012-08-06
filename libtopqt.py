#!/usr/bin/python3

import sqlite3 as lite
import subprocess
import sys
import os
import time
from threading import Thread

class KernelModuleHandler:
	modules = []

	def getLoadedModules(self):
		try:
			fileHandle = open("/proc/modules", "r")
		except:
			return None

		for line in fileHandle.read().split("\n"):
			#Ignore the last line
			if (line == ''): continue

			#Extract the data pieces
			col = line.split()

			self.modules.append({"name": col[0], "memory": col[1]})

		fileHandle.close()

		return self.modules

	def unloadModule(self, moduleName):
		call("rmmod " + moduleName)

class ProcessHandler:

	def killProcesses(self, processTuple):
		if processTuple is None: return

		killSignal = processTuple["signal"]

		for pid in processTuple["pidArray"]:
			os.kill(pid, killSignal)

	def killProcess(self, pid, sig):
		self.killProcesses({"signal": sig, "pidArray": [pid]})

	def getProcesses(self):
		psAUX = subprocess.getoutput('ps aux')
		processes = []
		
		for line in psAUX.split("\t"):
			columnHeadings = (line.split("\n")[0].split())
			values = line.split("\n")[1:]

			for colValues in values:
				psTuple =  {}
				for colNameNr in range(len(columnHeadings)):
					psTuple[columnHeadings[colNameNr]] = colValues.split()[colNameNr]
			
			
				if "[" in psTuple["COMMAND"]:
					psTuple["NAME"] = psTuple["COMMAND"]
				else:
					psTuple["NAME"] = psTuple["COMMAND"].split("/")[-1]
				#psTuple["NAME"] = psTuple["COMMAND"].split("/")[-1]
				processes.append(psTuple)
		return processes

class DatabaseHandler:
	_dbName = None
	_tblName = None
	
	def __init__(self,dbName, tblName):
		self._dbName = dbName
		self._tblName = tblName
	
	def createdb(self):
		connection = lite.connect(self._dbName)
		cur=connection.cursor()
		cur.execute("""CREATE TABLE ps(
		Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
		TimeStamp TEXT NOT NULL,
		User TEXT NOT NULL,
		Command TEXT NOT NULL,
		TTY TEXT NOT NULL,
		VSZ INTEGER NOT NULL,
		RSS INTEGER NOR NULL,
		CPU REAL NOT NULL,
		Memory NOT NULL
		);""")
		connection.commit()
		cur.close()
	
	def insertValue(self,columnValues):
		connection = lite.connect(self._dbName)
		cur=connection.cursor()
		print(columnValues)
		for psTuple in columnValues:
			TimeStamp = time.strftime("%Y.%m.%d@%H:%M:%S")
			User = psTuple["USER"]
			Command = psTuple["COMMAND"]
			TTY = psTuple["TTY"]
			VSZ = psTuple["VSZ"]
			RSS = psTuple["RSS"]
			CPU = psTuple["%CPU"]
			Memory = psTuple["%MEM"]
			cur.execute("""INSERT INTO ps(TimeStamp,User,Command,TTY,VSZ,RSS,CPU,Memory) VALUES(?,?,?,?,?,?,?,?)""",(TimeStamp,User,Command,TTY,VSZ,RSS,CPU,Memory))
		connection.commit()
		cur.close()
