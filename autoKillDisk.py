import sys
import os
import random
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QSpacerItem, QRadioButton, QGroupBox)
from PySide2.QtCore import Slot, Qt
import psutil
from psutil._common import bytes2human

class mainScreen(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.driveLabel = QLabel('Drive:')
        self.statusLabel = QLabel('Type:')
        self.checkLabel = QLabel('Master:')

        # TODO: Add a group box to make this look better

        self.layout = QGridLayout()

        self.layout.addWidget(self.driveLabel, 0, 0, 1, 2)
        self.layout.addWidget(self.statusLabel, 0, 3)
        self.layout.addWidget(self.checkLabel, 0, 5)

        self.drivesSet = 0
        self.driveNames = []
        self.driveStatus = []
        self.masterRadio = []
        for i in range(25):
            toAdd = QLabel('')
            self.driveNames.append(toAdd)
            toAdd2 = QLabel('')
            self.driveStatus.append(toAdd2)

        self.setWindowTitle('Auto Kill Disk')
        #icon = 
        #self.setWindowIcon()

    def addDrive(self, name, status):
        print('Index: ', self.drivesSet)
        self.driveNames[self.drivesSet].setText(name)
        self.driveStatus[self.drivesSet].setText(status)
        toSet = QRadioButton()
        self.layout.addWidget(toSet, self.drivesSet + 1, 5)
        self.drivesSet += 1       

    def addPayloadNames(self):
        for i in range(25):
            self.layout.addWidget(self.driveNames[i], i + 1, 0)
            self.layout.addWidget(self.driveStatus[i], i + 1, 3)

    def resetSpacing(self):
        self.layout.setContentsMargins(5, 5, 5, 5)

#Comes from https://github.com/giampaolo/psutil/blob/master/scripts/disk_usage.py
def getDisks(window):
    diskName = []
    diskUse = []
    diskTotal = []
    diskPercent = []
    counter = 0
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

    # Attempt using older idea
    '''
    dps = psutil.disk_partitions()
    fmt_str = "{:<8} {:<7} {:<7}"
    print(fmt_str.format("Drive", "Type", "Opts"))
    # Only show a couple of different types of devices, for brevity.
    for i in (0, 2):
        dp = dps[i]
        print(fmt_str.format(dp.device, dp.fstype, dp.opts))
        window.addDrive(dp.device, dp.fstype)
        '''

if __name__ == '__main__':
    print('We are running')
    main = QApplication(sys.argv)
    print('We are running')

    window = mainScreen()
    print('We are running')

    getDisks(window)
    print('We are running')

    #window.addDrive('SD2133654123', 'WIPED')
    #window.addDrive( 'SD2133654123', 'SETUP')
    window.resetSpacing()
    print('We are running')

    window.addPayloadNames()
    print('We are running')

    window.setLayout(window.layout)
    print('We are running')
    window.setFixedSize(300, 500)
    print('We are running')
    
    window.show()

    sys.exit(main.exec_())