from PyQt5.QtWidgets import *
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (QSize, pyqtSignal)
import sys
sys.path.append('../core/')
sys.path.append('../')
from Host import *
from arp import send_arp

import time, threading
import resources


def PARPThread(target, router, stopEvent):
    while(not stopEvent.is_set()):
        send_arp(target, router)
        time.sleep(1)

class HostWidget(QWidget):
    sig_closed = pyqtSignal(QWidget)

    def __init__(self, host):
        super(HostWidget, self).__init__()

        self.mitm = False

        self.host = host
        self.arpThread = None

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
        self.deleteButton.clicked.connect(self.onClose)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.ipText)
        hlayout.addWidget(self.nameText)
        hlayout.addWidget(self.macText)
        hlayout.addWidget(self.disconnectButton)
        hlayout.addWidget(self.poisoningButton)
        hlayout.addWidget(self.deleteButton)
        self.setLayout(hlayout)

    def stopAll(self):
        """This method stop all activity (destroy the thread and remove iptables rules)."""
        self.setMitM(False)
        self.setForward(False)

    def isInUse(self):
        """Returns true if the host is currently used (Poisoning or Disconnected), false otherwise."""
        if self.mitm:
            return True
        return False

    def onClose(self):
        """Slot called when the user click sur the close button. Close the host and emit a close signal. If the host is in use, display a message to the user to confirm."""
        closeHost = True
        if self.isInUse():
            buttonReply = QMessageBox.question(self, "Host in use", "The host" + str(self.host.ip) + " [" + str(self.host.mac) + "] is currently in use.\nDo you want to remove it anyway ?")
            if not buttonReply == QMessageBox.Yes:
                closeHost = False

        if closeHost:
            self.sig_closed.emit(self)

    def setMitM(self, value):
        """Active or desactive the MitM attack depending on the specified value."""
        if value:
            self.mitm = True
            if self.arpThread is None:
                self.arpThread_stop = threading.Event()
                self.arpThread = threading.Thread(target=PARPThread, args=(self.host, Host("192.168.1.1", "192.168.1.1", "192.168.1.1"), self.arpThread_stop))
                self.arpThread.start()
        else:
            self.mitm = False
            if self.arpThread is not None:
                self.arpThread_stop.set() # note that this doesn't really kill the thread, another method should be used later...
                self.arpThread = None
            print("not ARP")

    def setForward(self, value):
        """Active or desactive the trafic forwarding between target and router with iptable.
        If the forwarding is disabled, the target is disconnected to the router."""
        if value:
            print("forward")
        else:
            print("no forward")

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
            self.setForward(False)
            self.__setPoisoningChecked(False)
            self.__setDisconnectChecked(True)
        else:
            self.__setPoisoningChecked(False)
            self.__setDisconnectChecked(False)

    def onPoison(self, clicked):
        self.setMitM(clicked)
        if clicked:
            self.setForward(True)
            self.__setPoisoningChecked(True)
            self.__setDisconnectChecked(False)
        else:
            self.__setPoisoningChecked(False)
            self.__setDisconnectChecked(False)

class HostListWidget(QWidget):
    def __init__(self):
        super(HostListWidget, self).__init__()
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.hosts = []

    def refreshHosts(self, hosts):
        for host in hosts:
            # check for duplicates.
            hw = HostWidget(host)
            self.mainLayout.addWidget(hw)
            hw.sig_closed.connect(self.onHostClosed)

    def onHostClosed(self, host):
        host.deleteLater()
        self.mainLayout.removeWidget(host)
