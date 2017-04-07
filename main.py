from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QSettings, QSize,
        Qt, QTextStream)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
        QMessageBox, QTextEdit)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.createToolBars()

        self.loadSettings()

    def closeEvent(self, event):
        self.saveSettings()
        event.accept()

    def about(self):
        QMessageBox.about(self, "ARP Poisoning", self.tr("TODO()"))

    def scanSubnet(self):
        pass

    def createActions(self):
        rootFolder = QFileInfo(__file__).absolutePath()
        self.act_scanSubnet = QAction(QIcon(rootFolder + '/images/scanSubnet.png'), "&New", self, shortcut=QKeySequence.Refresh, statusTip="Scan subnet",
                triggered=self.scanSubnet)

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

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
