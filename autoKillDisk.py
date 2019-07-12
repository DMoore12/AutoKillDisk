import sys
import os
import random
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QSpacerItem, QRadioButton, QGroupBox, QProgressBar)
from PySide2.QtCore import Slot, Qt, QThread, QObject, pyqtSignal
#import psutil
#from psutil._common import bytes2human
import wmi
import subprocess
import time
from threading import Timer, Thread
import pythoncom

# Possible fix to the threading issue: https://stackoverflow.com/questions/36434706/pyqt-proper-use-of-emit-and-pyqtsignal
# Also, checkout fbs installer
# Also, https://pythonprogramming.net/menubar-pyqt-tutorial/?completed=/button-functions-pyqt-tutorial/
# Also, possible fix two: https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html
# TODO: Create a proper build script

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
        self.refactor = QPushButton('Refactor')

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
        self.layout.addWidget(self.wipeButton, 27, 2, 1, 2)
        self.layout.addWidget(self.cancelButton, 27, 4, 1, 2)
        self.layout.addWidget(self.bottomStatus, 28, 0, 1, 10)
        self.layout.addWidget(self.refactor, 27, 0, 1, 2)
        self.drivesSet = 0
        self.driveNames = []
        self.driveStatus = []
        self.driveSize = []
        self.drivePartitions = []
        self.driveIndex = []
        self.masterRadio = []
        self.master = self.getMaster()
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
        #icon = 
        #self.setWindowIcon()
        self.wipeButton.clicked.connect(self.startButtonClicked)
        self.refactor.clicked.connect(self.refactorDrives)

    def addDrive(self, name, status, size, partitions, index):
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

    def startButtonClicked(self):
        self.bottomStatus.setText('Are you sure you want to wipe?')
        self.confirmButton = QPushButton('Confirm')
        self.layout.addWidget(self.confirmButton, 27, 6, 1, 2)
        self.setLayout(self.layout)

        self.confirmButton.clicked.connect(self.getIndex)

    def setText(self):
        self.bottomStatus.setText('Ready to Wipe')

    def getIndex(self):
        self.confirmButton.deleteLater()
        self.bottomStatus.setText('Starting Wipe')
        self.indexToWipe = []
        self.serialToWipe = []
        for i in range(len(self.masterRadio)):
            if not self.masterRadio[i].isChecked():
                self.indexToWipe.append(self.index[i])
                self.serialToWipe.append(self.serial[i])
        if len(self.indexToWipe) == len(self.index):
            self.bottomStatus.setText('Error: No master drive selected!')
            self.refactorDrives()
            t = Timer(3, self.setText)
            t.start()
            return None
        elif len(self.indexToWipe) == 0:
            self.refactorDrives()
            self.bottomStatus.setText('No drives available to wipe!')
            t = Timer(3, self.setText)
            t.start()
        else:
            serialString = self.serialToWipe[0]
            for i in range(1, len(self.serialToWipe)):
                serialString += ', ' + self.serialToWipe[i]
            self.bottomStatus.setText('Wiping Drives:' + serialString)
            self.progress.setValue(self.progressInt)
            for i in range(len(self.masterRadio)):
                # TODO: Figure out which index is the master so we don't wipe it
                if self.masterRadio[i].isChecked():
                    self.driveStatus[i].setText('MASTER')
                else:
                    self.driveStatus[i].setText('WIPING')
            wipeDrives(self, self.indexToWipe)

    def refactorDrives(self):
        pythoncom.CoInitialize()
        for i in range(len(self.driveNames)):
            self.driveNames[i].setText('')
            self.driveStatus[i].setText('')
            self.driveSize[i].setText('')
            self.drivePartitions[i].setText('')
            self.driveIndex[i].setText('')
        for i in range(len(self.masterRadio)):
            self.masterRadio[i].deleteLater()
        self.setLayout(self.layout)
        del self.masterRadio
        self.masterRadio = []
        self.drivesSet = 0
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
        getDisks(self)
        self.addPayloadNames()
        self.setLayout(self.layout)

    def getMaster(self):
        exists = os.path.isfile('C:/config.txt')
        if not exists:
            self.bottomStatus.setText('Error: Config file not found. Defaulting to master drive with index 0.')
            t = Timer(5, self.setText)
            t.start()
            return 0
        with open('config.txt', 'r') as fh:
            for line in fh:
                toSet = line.strip(' ')
        self.bottomStatus.setText('Loading complete')
        t = Timer(5, self.setText)
        t.start()
        return toSet
    
    @pyqtSlot(int)
    def startRefactor(self):
        self.refactorDrives()

class refactorThread(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            self.window.refactorDrives()

class refSignal(QtCore.QObject):
    sig = pyqtSignal()
    self.sig.emit(1)

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
    print('Running')
    initialFiles = fileCount()
    increment = 90 / len(indexList)
    for index in indexList:
        #string = 'KillDisk -erasemethod=[3] -passes=[3] -verification=[10] -retryattempts=[5] -wipehdd=[' + index.strip(' ') + '] -noconfirmation'
        string = 'C:/"Program Files"/"LSoft Technologies"/"Active@ KillDisk Ultimate 11"/KillDisk.exe -erasemethod=3 -passes=3 -verification=25 -retryattempts=5 -erasehdd=' + str(index) + ' -cp=C:/Users/%USERNAME%/Desktop/"Certificate Output"/ -nc -bm\n'
        p = subprocess.Popen(string, stdout = subprocess.PIPE, shell = True)
        (output, err) = p.communicate()
        p_status = p.wait()
        files = fileCount()
        if not files == initialFiles:
            self.progressInt += increment
            self.progress.setValue(self.progressInt)
            initialFiles += 1
        else:
            toBreak = False
            while not toBreak:
                time.sleep(3000)
                files = fileCount()
                if fileCount == initialFiles:
                    self.progressInt += increment
                    self.progress.setValue(self.progressInt)
                    initialFiles += 1
                    toBreak = True
                    break

def fileCount():
    fileCount = 0
    for _, dirs, files in os.walk('C:/Users/%USERNAME%/Desktop/"Certificate Output"/'):
        fileCount += len(files)
    return fileCount

if __name__ == '__main__':
    main = QApplication(sys.argv)
    window = mainScreen()

    getDisks(window)

    window.resetSpacing()
    window.addPayloadNames()
    window.setLayout(window.layout)
    window.setFixedSize(500, 600)

    refThread = refactorThread(window)

    window.show()

    sys.exit(main.exec_())
