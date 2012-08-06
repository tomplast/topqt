#!/usr/bin/python3

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
