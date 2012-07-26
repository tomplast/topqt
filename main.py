#!/usr/bin/python3

import subprocess, sys
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
    window = uic.loadUi("ProgramA.ui");
    setupTable([{"caption": "PID", "key": "pid"}, {"caption":"Name","key":"name"},{"caption":"path","key":"path"}])
    psA = subprocess.getoutput('ps -A')
    
    
    
    f = open('psAResult','wt')
    f.write(psA)
    f.close()
    
    from_file = open('psAResult')
    testTuple = {}
    for line in from_file:
        col = line.split()
        testTuple["pid"] = col[0]
        testTuple["name"] = col[3]
        insertRow(testTuple)



    window.show();
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()