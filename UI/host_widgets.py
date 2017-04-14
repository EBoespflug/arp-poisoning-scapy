from PyQt5.QtWidgets import (QListWidget, QLineEdit, QListWidgetItem, QHBoxLayout, QVBoxLayout, QWidget)
import sys
sys.path.append('../core/')
from Host import *

class HostWidget(QWidget):
    def __init__(self, host):
        super(HostWidget, self).__init__()
        self.host = host
        self.nameText = QLineEdit()
        self.nameText.setReadOnly(True)
        self.nameText.setText(self.host.name)
        self.ipText = QLineEdit()
        self.ipText.setReadOnly(True)
        self.ipText.setText(self.host.ip)
        self.macText = QLineEdit()
        self.macText.setReadOnly(True)
        self.macText.setText(self.host.mac)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.ipText)
        hlayout.addWidget(self.nameText)
        hlayout.addWidget(self.macText)
        self.setLayout(hlayout)

class HostListWidget(QWidget):
    def __init__(self):
        super(HostListWidget, self).__init__()
        #self.hostsWidget
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

    def refreshHosts(self, hosts):
        for host in hosts:
            self.mainLayout.addWidget(HostWidget(host))

    def Clicked(self,item):
       pass
