'''
Created on May 28, 2010

@author: nikolavp
'''
from PyQt4 import QtCore
from PyQt4.QtGui import QMainWindow, QToolBar, QAction, QApplication, QWidget
from main_window import Ui_MainWindow


class GuiClient(QMainWindow, Ui_MainWindow):
    def __init__(self, mpd_api, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self);
        self.mpd_api = mpd_api
