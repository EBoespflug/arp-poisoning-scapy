from PyQt5.QtWidgets import (QListWidget, QHBoxLayout, QWidget)
import sys
sys.path.append('../core/')
from Host import *

class HostWidget(QWidget):
    def __init__(host):
        self.host = host
        self.mac = str(mac)
        self.name = str(name)
        self.on_use = False



class HostListWidget(QListWidget):

   def Clicked(self,item):
       pass
