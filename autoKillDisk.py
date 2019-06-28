import sys
import random
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QSpacerItem)
from PySide2.QtCore import Slot, Qt

class mainScreen(QWidget):
    def __init__(temp):
        QWidget.__init__(self)

        self.driveLabel = QLabel('Drive:')
        self.statusLabel = QLabel('Status:')
        self.checkLabel = QLabel('Master Drive:')

        self.layout = QGridLayout()

        self.layout.addWidget(self.driveLabel, 0, 0, 1, 2)
        self.layout.addWidget(self.statusLabel, 0, 3)
        self.layout.addWidget(self.checkLabel, 0, 5)

        self.drivesSet = 0
        self.driveNames = []
        self.driveStatus = []
        for i in range(8):
            toAdd = QLabel('')
            self.driveNames.append(toAdd)
            self.driveStatus.append(toAdd)

        self.setWindowTitle('Auto Kill Disk')
        #icon = 
        #self.setWindowIcon()

    def addDriveName(self, status):
        #self.driveNames[self.drivesSet].setText(name)
        print('Name Added: ', self.driveNames[self.drivesSet].text())
        self.driveStatus[self.drivesSet].setText(status)
        print('Name Added: ', self.driveNames[self.drivesSet].text())
        print('Status Added: ', status)
        self.drivesSet += 1

    def addDriveStatus(self, status)        

    def addPayloadNames(self):
        for i in range(8):
            self.layout.addWidget(self.driveNames[i], i + 1, 0)
            print('Part Two: Adding Name', self.driveNames[i].text())

    
    def addPayloadStatus(self):
        for i in range(8):
            self.layout.addWidget(self.driveStatus[i], i + 1, 3)

    def resetSpacing(self):
        self.layout.setContentsMargins(5, 5, 5, 5)

if __name__ == '__main__':
    main = QApplication(sys.argv)

    window = mainScreen()
    window.addDrive('SD2133654123', 'WIPED')
    window.addDrive(window, 'SD2133654123', 'SETUP')
    window.resetSpacing()
    window.addPayloadNames()
    window.addPayloadStatus()
    window.setLayout(window.layout)
    window.setFixedSize(300, 150)
    
    window.show()

    sys.exit(main.exec_())