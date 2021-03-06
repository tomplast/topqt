#!/usr/bin/python3

import configparser
import subprocess
import sys
import os
import time
from libtopqt import *
from threading import Thread
from PyQt4 import QtGui, uic
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
import gettext
import re

window = None
columnKeyBindings = None
selectedRowIndex = None
processNameFilter = "bash"

class SettingsDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.setWindowTitle('Settings')
		self.resize(300, 200)


class RefresherThread(QtCore.QThread):
	refreshFrequency = None
	
	def __init__(self, refreshFrequency):
		self.refreshFrequency = refreshFrequency
		QtCore.QThread.__init__(self)

	def run(self):
		while True:
			window.tableWidget.clearContents()
			for i in range(window.tableWidget.rowCount()-1, -1, -1):
				try:
					window.tableWidget.removeRow(i)
				except Exception:
					print("Här blev det fel" + i)
					
			getAndShowProcesses()
			time.sleep(self.refreshFrequency)


def setupTable(data):
	global columnKeyBindings
	columnKeyBindings = data
	tableWidget = window.tableWidget

	tableWidget.setColumnCount(len(columnKeyBindings))
	for binding in columnKeyBindings:
		tableWidget.setHorizontalHeaderItem(columnKeyBindings.index(binding), QtGui.QTableWidgetItem(binding["caption"]))


def insertRow(data):
	global columnKeyBindings
	searchIndex = -1;
	matchKey = None

	tableWidget = window.tableWidget
	tableWidget.setSortingEnabled(False)
	tableWidget.insertRow(tableWidget.rowCount())

	#tableWidget.insertRow(tableWidget.rowCount())

	for value in data:
		searchIndex = 0
		matchKey = None
		for binding in columnKeyBindings:
			searchIndex = searchIndex + 1
			if value == binding["key"]:
				matchKey = value
				break

		if matchKey:
			tableWidget.setItem(tableWidget.rowCount()-1, searchIndex-1, QtGui.QTableWidgetItem(data[matchKey]))

	#Ugly hack filter
	if not re.match('.*' + processNameFilter + '.*', data["NAME"]):
		print("WRONG")
		tableWidget.hideRow(1)

	tableWidget.setSortingEnabled(True)

def getAndShowProcesses():
	processHandler = ProcessHandler()	
	processes = processHandler.getProcesses()
	print("Found: {0} processes".format(len(processes)))
	for psTuple in processes:
		insertRow(psTuple)


def readConfig():
	#Used for translation

	#Fix translations
	keyToColumnNames = {"COMMAND": "Command", "USER": "Useless"}
	
	config = configparser.RawConfigParser()
	config.read('topqt.conf')
	
	setupTuple = []
	for c in config.get('general','columns').split(","):

		try:
			setupTuple.append({"caption": keyToColumnNames[c], "key": c})
		except:
			setupTuple.append({"caption": c, "key": c})
			pass

	setupTable(setupTuple)

def actionQuitTriggered():
	QtGui.QApplication.quit()


def actionSettingsTriggered():
	settingsDialog = SettingsDialog(window)
	settingsDialog.exec()

def itemSelectionChanged():
	pass
	#print(window.tableWidget.selectedIndexes()[0].row())
	#print(window.tableWidget.selectedItems())

def main():
	gettext.install('topqt')
	gettext.translation('topqt', './locale', languages=['sv']).install(True)
	
	global window
	app = QtGui.QApplication(sys.argv)
	if os.path.isfile("/usr/share/topqt/topqt.ui"):
		window = uic.loadUi("/usr/share/topqt/topqt.ui")
	elif os.path.isfile("topqt.ui"):
		window = uic.loadUi("topqt.ui")
	else:
		print(_("Error! Couldn't find user interface file topqt.ui! Aborting!"))
		sys.exit(1)
		
	readConfig()
	
	#setupTable([{"caption": "PID", "key": "PID"},{"caption":"Name","key":"NAME"}, {"caption":"%CPU","key":"%CPU"},{"caption":"path","key":"COMMAND"}])
	
	t = RefresherThread(5)
	t.start()

	window.connect(window.actionQuit, QtCore.SIGNAL("triggered()"), actionQuitTriggered);
	window.connect(window.actionSettings, QtCore.SIGNAL("triggered()"), actionSettingsTriggered);

	#window.tableWidget.connect(window.tableWidget, QtCore.SIGNAL('itemSelectionChanged()'), itemSelectionChanged)

	window.show();
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()
