from PyQt5.QtWidgets import (QListWidget, QLineEdit, QListWidgetItem, QHBoxLayout, QVBoxLayout, QPushButton, QWidget)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (QSize)
import sys
sys.path.append('../core/')
sys.path.append('../')
from Host import *
from arp import send_arp

import time, threading
import resources


def PARPThread(target, router):
    while(True):
        send_arp(target, router)
        time.sleep(1)

class HostWidget(QWidget):
    def __init__(self, host):
        super(HostWidget, self).__init__()

        self.mitm = False

        self.host = host
        self.arpTread = None

        self.createWidgets()

    def createWidgets(self):
        self.nameText = QLineEdit()
        self.nameText.setReadOnly(True)
        self.nameText.setText(self.host.name)
        self.ipText = QLineEdit()
        self.ipText.setReadOnly(True)
        self.ipText.setText(self.host.ip)
        self.macText = QLineEdit()
        self.macText.setReadOnly(True)
        self.macText.setText(self.host.mac)

        self.disconnectButton = QPushButton(QIcon(":/ico/connected"), "")
        self.disconnectButton.setCheckable(True)
        self.disconnectButton.clicked.connect(self.onDisconnect)
        self.poisoningButton = QPushButton(QIcon(":/ico/notPoisoning"), "")
        self.poisoningButton.setCheckable(True)
        self.poisoningButton.clicked.connect(self.onPoison)
        self.deleteButton = QPushButton(QIcon(":/ico/delete"), "")

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.ipText)
        hlayout.addWidget(self.nameText)
        hlayout.addWidget(self.macText)
        hlayout.addWidget(self.disconnectButton)
        hlayout.addWidget(self.poisoningButton)
        hlayout.addWidget(self.deleteButton)
        self.setLayout(hlayout)

    def setMitM(self, value):
        """Active or desactive the MitM attack depending on the specified value."""
        if value:
            print("ARP")
        else:
            print("not ARP")

    def __setPoisoningChecked(self, value):
        if value:
            self.poisoningButton.setIcon(QIcon(":/ico/poisoning"))
            self.poisoningButton.setChecked(True)
        else:
            self.poisoningButton.setIcon(QIcon(":/ico/notPoisoning"))
            self.poisoningButton.setChecked(False)

    def __setDisconnectChecked(self, value):
        if value:
            self.disconnectButton.setIcon(QIcon(":/ico/disconnected"))
            self.disconnectButton.setChecked(True)
        else:
            self.disconnectButton.setIcon(QIcon(":/ico/connected"))
            self.disconnectButton.setChecked(False)

    def onDisconnect(self, clicked):
        self.setMitM(clicked)
        if clicked:
            self.__setPoisoningChecked(False)
            self.__setDisconnectChecked(True)
        else:
            self.__setPoisoningChecked(False)
            self.__setDisconnectChecked(False)

    def onPoison(self, clicked):
        self.setMitM(clicked)
        if clicked:
            self.__setPoisoningChecked(True)
            self.__setDisconnectChecked(False)
        else:
            self.__setPoisoningChecked(False)
            self.__setDisconnectChecked(False)

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
