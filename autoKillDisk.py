    
import sys
import os
import random
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QSpacerItem, QRadioButton, QGroupBox, QProgressBar)
from PySide2.QtCore import Slot, Qt
#import psutil
#from psutil._common import bytes2human
import wmi

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
        self.bottomStatus = QLabel('Ready to Wipe')

        # TODO: Add a group box to make this look better
        # EDIT TODO: Use GUI application to build a really good looking app!
        # TODO: Add selection of wipe method, verification, and certificate output

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
        #icon = 
        #self.setWindowIcon()
        self.wipeButton.clicked.connect(self.startButtonClicked)

    def addDrive(self, name, status, size, partitions, index):
        self.driveNames[self.drivesSet].setText(name)
        self.driveStatus[self.drivesSet].setText(status)
        self.driveSize[self.drivesSet].setText(size + ' GB')
        self.drivePartitions[self.drivesSet].setText(str(partitions))
        self.driveIndex[self.drivesSet].setText(str(index))
        toSet = QRadioButton()
        self.masterRadio.append(toSet)
        self.layout.addWidget(self.masterRadio[self.drivesSet], self.drivesSet + 1, 9)
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

    def startButtonClicked(self):
        self.bottomStatus.setText('Are you sure you want to wipe?')
        self.confirmButton = QPushButton('Confirm')
        self.layout.addWidget(self.confirmButton, 27, 4, 1, 2)
        self.setLayout(self.layout)

        self.confirmButton.clicked.connect(self.getIndex)

    def getIndex(self):
        self.confirmButton.deleteLater()
        self.bottomStatus.setText('Starting Wipe')
        self.indexToWipe = []
        self.serialToWipe = []
        for i in range(len(self.masterRadio)):
            # TODO: Figure out which index is the master so we don't wipe it
            if self.masterRadio[i].isChecked():
                self.driveStatus[i].setText('MASTER')
            else:
                self.indexToWipe.append(self.index[i])
                self.serialToWipe.append(self.serial[i])
                self.driveStatus[i].setText('WIPING')
        if len(self.indexToWipe) == len(self.index):
            self.bottomStatus.setText('Error: No master drive selected!')

            # TODO: Write the refactoring function

            self.refactorDrives()
            return None
        if len(self.indexToWipe) != 0:
            serialString = self.serialToWipe[0]
            for i in range(1, len(self.serialToWipe)):
                serialString += ', ' + self.serialToWipe[i]
            self.bottomStatus.setText('Wiping Drives:' + serialString)
            self.progress.setValue(10)
            wipeDrives(self, self.indexToWipe)

    def refactorDrives(self):
        print('Still need to write this!')

#Comes from https://github.com/giampaolo/psutil/blob/master/scripts/disk_usage.py
def getDisks(window):
    counter = 0
    window.index = []
    window.serial = []
    c = wmi.WMI()
    for pm in c.Win32_DiskDrive():
        #print(pm.SerialNumber, pm.Name, pm.Size, pm.Status, pm.SystemName, pm.Signature, pm.Partitions)
        window.addDrive(pm.SerialNumber.strip(' '), pm.Status, str(round( (int(pm.Size) / 1000000000), 2)), pm.Partitions, pm.Index)
        window.index.append(pm.Index)
        window.serial.append(pm.SerialNumber.strip(' '))

def wipeDrives(parent, indexList):
    increment = 90 / len(indexList)
    for index in indexList:
        #string = 'KillDisk -erasemethod=[3] -passes=[3] -verification=[10] -retryattempts=[5] -wipehdd[' + index.strip(' ') + '] -noconfirmation'
        string = 'KillDisk.exe -erasemethod=[3] -passes=[3] -verification=[10] -retryattempts=[5] -wipehdd[' + str(index) + '] -noconfirmation\n'
        # TODO: Get abs path of KillDisk and use shortened versions of flags
        print(string)
        os.system(string)

if __name__ == '__main__':
    main = QApplication(sys.argv)
    window = mainScreen()

    getDisks(window)

    window.resetSpacing()
    window.addPayloadNames()
    window.setLayout(window.layout)
    window.setFixedSize(500, 600)

    window.show()

    sys.exit(main.exec_())