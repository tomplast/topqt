#!/usr/bin/python3
import sys
from PyQt4 import QtCore, QtGui, uic

window = None
columnKeyBindings = None

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
	tableWidget.insertRow(tableWidget.rowCount())

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
	
	#tableWidget.setItem(tableWidget.rowCount()-1, 0, QtGui.QTableWidgetItem(data["pid"]))
	#tableWidget.setItem(tableWidget.rowCount()-1, 1, QtGui.QTableWidgetItem(data["name"]))


def main():
	global window
	app = QtGui.QApplication(sys.argv)
	window = uic.loadUi("ProgramA.ui");

	#setupTable([{"caption": "Name", "key": "name"}, {"caption": "PID", "key": "pid"}])
	#setupTable([{"caption": "PID", "key": "pid"}, {"caption": "Name", "key": "name"}])
	setupTable([{"caption": "PID", "key": "pid"}])

	insertRow({"pid": "1", "name": "/usr/bin/vncserver"})
	insertRow({"pid": "2", "name": "bash"})
	insertRow({"pid": "3", "name": "sh"})

	window.show();



#window.treeWidget.hide()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()


