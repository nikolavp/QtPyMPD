# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Sun Jun 13 12:13:21 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalSlider = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickPosition(QtGui.QSlider.NoTicks)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout.addWidget(self.horizontalSlider, 0, 0, 1, 2)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.playlistsTab = QtGui.QWidget()
        self.playlistsTab.setObjectName("playlistsTab")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.playlistsTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listView = QtGui.QListView(self.playlistsTab)
        self.listView.setObjectName("listView")
        self.verticalLayout_3.addWidget(self.listView)
        self.tabWidget.addTab(self.playlistsTab, "")
        self.libraryTab = QtGui.QWidget()
        self.libraryTab.setObjectName("libraryTab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.libraryTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtGui.QLineEdit(self.libraryTab)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.treeView = QtGui.QTreeView(self.libraryTab)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.libraryTab, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableView.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.gridLayout.addWidget(self.tableView, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionSettings = QtGui.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.actionToggle = QtGui.QAction(MainWindow)
        self.actionToggle.setObjectName("actionToggle")
        self.actionStop = QtGui.QAction(MainWindow)
        self.actionStop.setObjectName("actionStop")
        self.actionPrev = QtGui.QAction(MainWindow)
        self.actionPrev.setObjectName("actionPrev")
        self.actionNext = QtGui.QAction(MainWindow)
        self.actionNext.setObjectName("actionNext")
        self.menuFile.addAction(self.actionExit)
        self.menu_Help.addAction(self.action_About)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.actionPrev)
        self.toolBar.addAction(self.actionToggle)
        self.toolBar.addAction(self.actionNext)
        self.toolBar.addAction(self.actionStop)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL("triggered()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.playlistsTab), QtGui.QApplication.translate("MainWindow", "Playlists", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.libraryTab), QtGui.QApplication.translate("MainWindow", "Library", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "&Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToggle.setText(QtGui.QApplication.translate("MainWindow", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToggle.setToolTip(QtGui.QApplication.translate("MainWindow", "Start playing", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToggle.setShortcut(QtGui.QApplication.translate("MainWindow", "Meta+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop.setText(QtGui.QApplication.translate("MainWindow", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop.setToolTip(QtGui.QApplication.translate("MainWindow", "Stop the music", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop.setShortcut(QtGui.QApplication.translate("MainWindow", "Meta+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrev.setText(QtGui.QApplication.translate("MainWindow", "Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNext.setText(QtGui.QApplication.translate("MainWindow", "Next", None, QtGui.QApplication.UnicodeUTF8))

