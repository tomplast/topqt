#!/usr/bin/python3

import subprocess, sys, os
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


def main():
    global window
    app = QtGui.QApplication(sys.argv)
    if os.path.isfile("/usr/share/topqt/topqt.ui"):
        window = uic.loadUi("/usr/share/topqt/topqt.ui")
    elif os.path.isfile("topqt.ui"):
        window = uic.loadUi("topqt.ui")
    else:
        print("Error! Couldn't find user interface file. Aborting!")
        sys.exit(1)
    
    setupTable([{"caption": "PID", "key": "PID"},{"caption":"Name","key":"NAME"}, {"caption":"%CPU","key":"%CPU"},{"caption":"path","key":"COMMAND"}])
    
    psAUX = subprocess.getoutput('ps aux')
    psTuple = {}
    for line in psAUX.split("\t"):
        columnHeadings = (line.split("\n")[0].split())
        values = line.split("\n")[1:]
        
        for colValues in values:
            for colNameNr in range(len(columnHeadings)):
                psTuple[columnHeadings[colNameNr]] = colValues.split()[colNameNr]
            
            print(psTuple)
            psTuple["NAME"] = psTuple["COMMAND"].split("/")[-1]
            insertRow(psTuple)

    window.show();
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
