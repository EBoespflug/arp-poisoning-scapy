from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QSettings, QSize,
        Qt, QTextStream)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QHBoxLayout, QAction, QApplication, QFileDialog, QMainWindow, QMessageBox, QTextEdit, QMessageBox)

import sys, os
sys.path.append('core/')
sys.path.append('UI/')

from Host import *
from scan_subnet import *
from host_widgets import *
from scapy.all import conf
import resources

conf.verb = 0

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createWidgets()

        self.loadSettings()
        self.setMinimumSize(800, 600)

        if os.geteuid() != 0:
            print("WARNING: The application seems have been launched without root privilege.")
            QMessageBox.warning(self, "Invalid privileges", "The application seems to have been launched without root privileges.\nPlease restart the appplication with sudo to access to all features.")

    def about(self):
        QMessageBox.about(self, "ARP Poisoning", self.tr("TODO()"))

    def scanSubnet(self):
        hosts = arping("192.168.1.*")
        print(hosts)
        self.hostList.refreshHosts(hosts)

    def createActions(self):
        rootFolder = QFileInfo(__file__).absolutePath()
        self.act_scanSubnet = QAction(QIcon(rootFolder + '/ico/scan'), "&New", self, shortcut=QKeySequence.Refresh, statusTip="Scan subnet", triggered=self.scanSubnet)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("Scan")
        self.fileToolBar.addAction(self.act_scanSubnet)

    def loadSettings(self):
        self.settings = QSettings("EBoespflug", "arp_poisoning_scapy")
        if not self.settings.value("MainWindow/geometry") == None:
            self.restoreGeometry(self.settings.value("MainWindow/geometry"))
        if not self.settings.value("MainWindow/state") == None:
            self.restoreState(self.settings.value("MainWindow/state"))

    def saveSettings(self):
        self.settings = QSettings("EBoespflug", "arp_poisoning_scapy")
        self.settings.setValue("MainWindow/geometry", self.saveGeometry())
        self.settings.setValue("MainWindow/state", self.saveState())

    def createWidgets(self):
        self.hostList = HostListWidget()
        self.setCentralWidget(self.hostList)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
