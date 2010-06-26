'''
Created on May 28, 2010
@author: nikolavp
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from main_window import Ui_MainWindow
DEFAULT_LIB_PATH = "/var/lib/mpd/music/"

class playlist_model(QAbstractTableModel):
    """A model to represent the playlist in the gui"""
    def __init__(self, mpd_api, parent):
        QAbstractTableModel.__init__(self, parent)
        self.playlist = mpd_api.playlistinfo()
        self.header_data = list(self.playlist[0].keys())

    def rowCount(self, parent):
        return len(self.playlist)

    def columnCount(self, parent):
        return len(self.header_data)

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        return self.playlist[index.row()][self.header_data[index.column()]]

    def headerData(self, column, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header_data[column]
        return None


class playlists_model(QAbstractListModel):
    """A model class to represent the saved playlists in the gui"""
    def __init__(self, playlists, parent):
        self.playlists = playlists

    def rowCount(self, parent):
        return len(self.playlists)

    def data(self, index, role):
        if not index.isvalid() or role != Qt.DisplayRole:
            return None
        return self.playlists[index.row()]

class gui_client(QMainWindow, Ui_MainWindow):
    """The gui client for mpd"""
    def __init__(self, mpd_api, parent=None):
        self.mpd_api = mpd_api
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        status = self.mpd_api.status()
        if status['state'] == 'play':
            self.actionToggle.setText('Pause')
        else:
            self.actionToggle.setText('Play')

        self.actionToggle.triggered.connect(lambda: self.toggle_handle())
        self.actionStop.triggered.connect(lambda: self.stop_handle())
        self.actionPrev.triggered.connect(lambda: self.mpd_api.previous())
        self.actionNext.triggered.connect(lambda: self.mpd_api.next())
        self.libraryModel = QFileSystemModel(self)
        self.libraryModel.setReadOnly(False)
        #TODO This is using a hardcoded string that should 
        #be changeable in other releases
        index = self.libraryModel.setRootPath(DEFAULT_LIB_PATH)
        self.treeView.setModel(self.libraryModel)
        self.treeView.setRootIndex(index)
        self.playlist = playlist_model(mpd_api, self)
        self.tableView.setModel(self.playlist)

    def stop_handle(self):
        self.playing = False
        self.mpd_api.stop()
        self.actionToggle.setText('Play')

    def toggle_handle(self):
        if 'Play' == str(self.actionToggle.text()):
            self.mpd_api.play()
            self.actionToggle.setText('Pause')
        else:
            self.mpd_api.pause()
            self.actionToggle.setText('Play')
