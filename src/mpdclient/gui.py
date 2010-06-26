'''
Created on May 28, 2010
@author: nikolavp
'''

from PyQt4.Qt import QAbstractListModel, Qt, QMainWindow, QFileSystemModel, \
    QAbstractTableModel, QAbstractItemView, QItemSelectionModel
from mpdclient.main_window import Ui_MainWindow

DEFAULT_LIB_PATH = "/var/lib/mpd/music/"

class playlist_model(QAbstractTableModel):
    """A model to represent the playlist in the gui"""
    def __init__(self, mpd_api, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.playlist = mpd_api.playlistinfo()
        self.header_data = list(self.playlist[0].keys())
        
    def rowCount(self, parent):
        return len(self.playlist)

    def columnCount(self, parent):
        return len(self.header_data)

    def get_row(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        return self.playlist[index.row()]

    def data(self, index, role):
        row = self.get_row(index, role)
        return None if row is None else row[self.header_data[index.column()]]

    def headerData(self, column, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header_data[column]
        return None


class playlists_model(QAbstractListModel):
    """A model class to represent the saved playlists in the gui"""
    def __init__(self, playlists, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.playlists = playlists

    def rowCount(self, parent):
        return len(self.playlists)

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        return self.playlists[index.row()]

class library_model(QAbstractListModel):
    def __init__(self, database, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.database = database
    def rowCount(self, parent):
        return len(self.database)

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        return self.database[index.row()]

class gui_client(QMainWindow, Ui_MainWindow):
    def __init__(self, mpd_api, parent=None):
        QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.mpd_api = mpd_api
        status = self.mpd_api.status()
        if status['state'] == 'play':
            self.actionToggle.setText('Pause')
        else:
            self.actionToggle.setText('Play')

        self.actionToggle.triggered.connect(self.toggle_handle)
        self.actionStop.triggered.connect(self.stop_handle)
        #Explicitly tell Qt that we don't accept any arguments 
        self.actionPrev.triggered.connect(self.play_previous)
        self.actionNext.triggered.connect(self.playnext)
        self.searchDirLib.textEdited.connect(self.filter_files)
        self.searchLib.textEdited.connect(self.filter_database_songs)

        self.libraryDirModel = QFileSystemModel(self)
        self.libraryDirModel.setReadOnly(False)
        self.libraryDirModel.setNameFilterDisables(False)
        #TODO: This is using a hardcoded string that should 
        #be changeable in other releases
        index = self.libraryDirModel.setRootPath(DEFAULT_LIB_PATH)
        self.treeView.setModel(self.libraryDirModel)
        self.treeView.setRootIndex(index)

        self.playlists = playlists_model(self._get_playlists() , self)
        self.listView.setModel(self.playlists)

        self.playlist = playlist_model(mpd_api, self)
        self.tableView.setModel(self.playlist)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.activated.connect(self.play_song)
        
        self.filter_database_songs(None)


    def filter_files(self, value):
        if value is None or value == '':
            self.libraryDirModel.setNameFilters([])
        else:
            self.libraryDirModel.setNameFilters(['*' + value + '*'])

    def filter_database_songs(self, value):
        if value is None or value == '':
            self.libraryModel = library_model(self._get_database_info(), self)
        else:
            matching_songs = self.mpd_api.search('any', value)
            matching_songs = list(map(lambda x: x['file'], matching_songs))
            self.libraryModel = library_model(matching_songs, self)
        self.libraryDatabase.setModel(self.libraryModel)


    def play_song(self, index):
        id = self.playlist.get_row(index, Qt.DisplayRole)
        self.mpd_api.playid(id['id'])

    def _get_database_info(self):
        all_songs_info = self.mpd_api.listallinfo()
        all_songs = list(map(lambda x: x['file'], all_songs_info))
        return all_songs

    def _get_playlists(self):
        resources = self.mpd_api.lsinfo()
        playlists = filter(lambda x: 'playlist' in x.keys(), resources)
        playlists = list(map(lambda x: x['playlist'], playlists))
        return playlists

    def stop_handle(self):
        self.mpd_api.stop()
        self.actionToggle.setText('Play')

    def select_index_from_current(self, dist):
        selection_model = self.tableView.selectionModel()
        currentsong = self.mpd_api.currentsong()
        next_index = self.playlist.index(int(currentsong['pos']) + dist, 0)
        selection_model.select(next_index, QItemSelectionModel.ClearAndSelect
                | QItemSelectionModel.Rows)

    def playnext(self):
        self.select_index_from_current(+1)
        self.mpd_api.next()
        self.treeView.setModel(self.libraryDirModel)

    def play_previous(self):
        self.select_index_from_current(-1)
        self.mpd_api.previous()

    def toggle_handle(self):
        if 'Play' == self.actionToggle.text():
            self.mpd_api.play()
            self.actionToggle.setText('Pause')
        else:
            self.mpd_api.pause()
            self.actionToggle.setText('Play')
