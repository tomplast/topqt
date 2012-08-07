#!/usr/bin/python3

import calendar
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
		TimeStamp INTEGER NOT NULL,
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
	
	def insertValueToDatabase(self,columnValues):
		connection = lite.connect(self._dbName)
		cur=connection.cursor()
		for psTuple in columnValues:
			TimeStamp = int(time.time())
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

	def getAllValueFromDatabase(self,columnValues):
		returnValue = []
		connection = lite.connect(self._dbName)
		cur=connection.cursor()
		for values in cur.execute("SELECT * FROM ps").fetchall():
			returnValue.append(values)
		connection.commit()
		cur.close()
		return returnValue

	def returnTimeToInt(self,timeStamp):
		date = timeStamp.split(" ")[0].split("-")
		time = timeStamp.split(" ")[1].split(":")
		tmpDataTime = date + time
		mergeData = []
		for timeMerge in tmpDataTime:
			mergeData.append(int(timeMerge))
		return calendar.timegm(tuple(mergeData))


	def getValuesFromDatabase(self,stTime,enTime):
		returnValue = []
		connection = lite.connect(self._dbName)
		cur = connection.cursor()
		sql = """SELECT * FROM ps 
				WHERE 
				TimeStamp >= {0} 
				AND 
				TimeStamp <= {1}""" .format(stTime,enTime)
		print(sql)
		cur.execute(sql)
		connection.commit()
		cur.close()
