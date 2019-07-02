    
import sys
import os
import random
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QSpacerItem, QRadioButton, QGroupBox)
from PySide2.QtCore import Slot, Qt
import psutil
from psutil._common import bytes2human
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

        # TODO: Add a group box to make this look better

        self.layout = QGridLayout()

        self.layout.addWidget(self.driveLabel, 0, 0, 1, 2)
        self.layout.addWidget(self.sizeLabel, 0, 3)
        self.layout.addWidget(self.statusLabel, 0, 5)
        self.layout.addWidget(self.partitionLabel, 0, 6)
        self.layout.addWidget(self.indexLabel, 0, 7)
        self.layout.addWidget(self.checkLabel, 0, 8)

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

    def addDrive(self, name, status, size, partitions, index):
        self.driveNames[self.drivesSet].setText(name)
        self.driveStatus[self.drivesSet].setText(status)
        self.driveSize[self.drivesSet].setText(size + ' GB')
        self.drivePartitions[self.drivesSet].setText(str(partitions))
        self.driveIndex[self.drivesSet].setText(str(index))
        toSet = QRadioButton()
        self.layout.addWidget(toSet, self.drivesSet + 1, 8)
        self.drivesSet += 1       

    def addPayloadNames(self):
        for i in range(25):
            self.layout.addWidget(self.driveNames[i], i + 1, 0, 1, 2)
            self.layout.addWidget(self.driveStatus[i], i + 1, 5, 1, 2)
            self.layout.addWidget(self.driveSize[i], i + 1, 3)
            self.layout.addWidget(self.drivePartitions[i], i + 1, 6)
            self.layout.addWidget(self.driveIndex[i], i + 1, 7)

    def resetSpacing(self):
        self.layout.setContentsMargins(5, 5, 5, 5)

#Comes from https://github.com/giampaolo/psutil/blob/master/scripts/disk_usage.py
def getDisks(window):
    #diskName = []
    #diskUse = []
    #diskTotal = []
    #diskPercent = []
    #counter = 0
    '''
    for part in psutil.disk_partitions(all=False):
        if counter < 25:
            if part.device == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            if not 'loop' in part.device:
                usage = psutil.disk_usage(part.mountpoint)
                diskName.append(part.device)
                diskTotal.append(bytes2human(usage.total))
                diskPercent.append(int(usage.percent))
                window.addDrive(diskName[counter], str(diskPercent[counter]))
                counter += 1
    '''
    c = wmi.WMI()
    for pm in c.Win32_DiskDrive():
        #print(pm.SerialNumber, pm.Name, pm.Size, pm.Status, pm.SystemName, pm.Signature, pm.Partitions)
        window.addDrive(pm.SerialNumber.strip(' '), pm.Status, str(round( (int(pm.Size) / 1000000000), 2)), pm.Partitions, pm.Index)

if __name__ == '__main__':
    main = QApplication(sys.argv)
    window = mainScreen()

    getDisks(window)

    window.resetSpacing()
    window.addPayloadNames()
    window.setLayout(window.layout)
    window.setFixedSize(500, 500)
    
    window.show()

    sys.exit(main.exec_())