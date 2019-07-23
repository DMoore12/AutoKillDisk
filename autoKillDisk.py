import sys
import random
import wmi
import subprocess
import time
import pythoncom
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QRadioButton, QProgressBar)
from PySide2 import QtCore
from threading import Timer, Thread

class mainScreen(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.driveLabel = QLabel('Serial Number:')
        self.sizeLabel = QLabel('Size:')
        self.statusLabel = QLabel('Status:')
        self.partitionLabel = QLabel('Partitions:')
        self.indexLabel = QLabel('Index:')
        self.checkLabel = QLabel('Master:')
        self.progress = QProgressBar()
        self.wipeButton = QPushButton('Wipe')
        self.cancelButton = QPushButton('Cancel')
        self.bottomStatus = QLabel('Load Complete')

        self.layout = QGridLayout()
        self.layout.addWidget(self.driveLabel, 0, 0, 1, 2)
        self.layout.addWidget(self.sizeLabel, 0, 3)
        self.layout.addWidget(self.statusLabel, 0, 5, 1, 2)
        self.layout.addWidget(self.partitionLabel, 0, 7)
        self.layout.addWidget(self.indexLabel, 0, 8)
        self.layout.addWidget(self.checkLabel, 0, 9)
        self.layout.addWidget(self.progress, 26, 0, 1, 10)
        self.layout.addWidget(self.wipeButton, 27, 0, 1, 2)
        self.layout.addWidget(self.cancelButton, 27, 2, 1, 2)
        self.layout.addWidget(self.bottomStatus, 28, 0, 1, 10)
        self.drivesSet = 0
        self.driveNames = []
        self.driveStatus = []
        self.driveSize = []
        self.drivePartitions = []
        self.driveIndex = []
        self.masterRadio = []
        self.progressInt = 10
        for i in range(25):
            toAdd = QLabel('')
            self.driveNames.append(toAdd)
            toAdd2 = QLabel('')
            self.driveSize.append(toAdd2)
            toAdd3 = QLabel('')
            self.driveStatus.append(toAdd3)
            toAdd4 = QLabel('')
            self.drivePartitions.append(toAdd4)
            toAdd5 = QLabel('')
            self.driveIndex.append(toAdd5)
        self.setWindowTitle('Auto Kill Disk')

        #TODO: Write the startWipe() function outside the class to remove from Qt GUI thread

        self.wipeButton.clicked.connect(startWipe)

        #TODO: Write the cancelWipe() function

        self.cancelButton.clicked.connect(cancelWipe)

        #TODO: Add threading call here
        initThread = initThread()
        self.initThread.connect(self.setMaster)

    def addDrive(self, name, status, size, partitions, index):

        #TODO: Rewrite this function to work from a non GUI thread and add bool for master

        self.driveNames[self.drivesSet].setText(name)
        self.driveStatus[self.drivesSet].setText(status)
        self.driveSize[self.drivesSet].setText(size + ' GB')
        self.drivePartitions[self.drivesSet].setText(str(partitions))
        self.driveIndex[self.drivesSet].setText(str(index))
        toAdd = QRadioButton()
        self.masterRadio.append(toAdd)
        self.layout.addWidget(self.masterRadio[self.drivesSet], self.drivesSet + 1, 9)
        if int(index) == int(self.master):
            self.masterRadio[self.drivesSet].setChecked(True)
        self.drivesSet += 1  

    def addPayloadNames(self):
        for i in range(25):
            self.layout.addWidget(self.driveNames[i], i + 1, 0, 1, 2)
            self.layout.addWidget(self.driveStatus[i], i + 1, 5, 1, 2)
            self.layout.addWidget(self.driveSize[i], i + 1, 3)
            self.layout.addWidget(self.drivePartitions[i], i + 1, 7)
            self.layout.addWidget(self.driveIndex[i], i + 1, 8)

    def resetSpacing(self):
        self.layout.setContentsMargins(10, 10, 0, 10)

    #TODO: Add the signal and slot to make this call work properly

    def setText(self, text):
        self.bottomStatus.setText(text)

    def resetLabels(self):
        for i in range(25):
            toAdd = QLabel('')
            self.driveNames.append(toAdd)
            toAdd2 = QLabel('')
            self.driveSize.append(toAdd2)
            toAdd3 = QLabel('')
            self.driveStatus.append(toAdd3)
            toAdd4 = QLabel('')
            self.drivePartitions.append(toAdd4)
            toAdd5 = QLabel('')
            self.driveIndex.append(toAdd5)
        self.addPayloadNames()
        self.setLayout(self.layout)

    #TODO: Add the signal and slot to make the master set with logic outside the GUI thread
    #TODO: Remember that the index for the masterRadio list and that something neeeds to be done outside the GUI thread to get by this
    #TODO: It could also be done where each drive has a master status when it gets added, but that should be done later

    def setMaster(self, masterInt):
        try:
            self.masterRadio[masterInt].setChecked()
        except:
            print('The given master was outside the range of given ones')

class initial(Thread):
    masterFoundSig = QtCore.Signal(int)

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        # All initialization tasks not related to the GUI should go here
        try:
            with open('config.txt') as fh:
                for line in fh:
                    master = int(line)
            self.masterFoundSig.emit(master)
        except:
            print('Config file was unable to be opened!')

class refactor(Thread):

    def __init(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        #TODO: Add drive refactoring stuff
        #NOTE: It should be fine to just get all the drives all the time, but it would be nice to gather some info so we don't have to do it every time
            # Maybe just get the number of drives and compare?
            # Then every so often just run the whole refactor in case someone pulls a fast one on us?
        
if __name__ == '__main__':
    main = QApplication(sys.argv)
    window = mainScreen()

    window.resetSpacing()
    window.addPayloadNames()
    window.setLayout(window.layout)
    window.setFixedSize(500, 600)
