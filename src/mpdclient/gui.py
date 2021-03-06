'''
Created on May 28, 2010
@author: nikolavp
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from main_window import Ui_MainWindow

DEFAULT_LIB_PATH = "/var/lib/mpd/music/"
FILE_TYPE = "application/file"
#The data fields that will be showed in the playlist
PLAYLIST_HEADER_DATA = ['Title', 'Artist', 'Album', 'Track', 'Time', 'Disc']

class playlist_model(QAbstractTableModel):
    """A model to represent the playlist in the gui"""
    def __init__(self, mpd_api, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.mpd_api = mpd_api
        self.playlistinfo = self.mpd_api.playlistinfo()
        self.header_data = PLAYLIST_HEADER_DATA
        self.current_song_pos = -1

    def update_current_song(self, pos):
        """Update the current song so it can have a nice dark background
        when the view get it with the data function"""
        self.current_song_pos = int(pos)
        self.reset()

    def setData(self, index, val, parent = None):
        self.playlistinfo[index.row()] = val
        self.emit(SIGNAL("dataChanged"), index, index)

    def rowCount(self, parent = None):
        return len(self.playlistinfo)

    def columnCount(self, parent = None):
        return len(self.header_data)

    def get_song(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        return self.playlistinfo[index.row()]

    def modify_field(self, field, value):
        """Modify some fields before showing them in the view"""
        if field == 'time':
            seconds = int(value)
            if seconds > 60:
                return str(seconds // 60) + ":" + str(seconds % 60)
            else:
                return value
        return value

    def data(self, index, role):
        if role == Qt.BackgroundRole and index.row() == self.current_song_pos:
            return QPalette().color(QPalette.Dark)
        if role == Qt.DisplayRole:
            row = self.get_song(index, role)
            if row is not None:
                field = self.header_data[index.column()].lower()
                if field in row.keys():
                    return self.modify_field(field, row[field])

    def headerData(self, column, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header_data[column]

    def flags(self, index):
        default_flags = QAbstractTableModel.flags(self, index)
        if index.isValid():
            return default_flags | Qt.ItemIsDropEnabled
        else:
            return default_flags | Qt.ItemIsDropEnabled

    def insertRows(self, row, count, parent = None):
        self.beginInsertRows(QModelIndex(), row, row+count - 1)
        self.playlistinfo[row:row] = [None] * count
        self.endInsertRows()

    def mimeTypes(self):
        return [FILE_TYPE]

    def dropMimeData(self, data, action, row, column, parent = None):
        if action == Qt.IgnoreAction:
            return True

        if not data.hasFormat(FILE_TYPE):
            return False
        dropped_data = data.data(FILE_TYPE).split('\n')

        if parent.row() == -1:
            c = len(self.playlistinfo)
        else:
            c = parent.row()
        self.insertRows(c, len(dropped_data))
        for record in dropped_data:
            record = str(record).rstrip("'").lstrip("b'")
            id = self.mpd_api.addid(record, c)
            song_data = self.mpd_api.playlistid(id)
            index = self.index(c, 0)
            self.setData(index, song_data[0])
            c+=1
        return True

class playlists_model(QAbstractListModel):
    """A model class to represent the saved playlists in the gui"""
    def __init__(self, playlists, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.playlists = playlists

    def rowCount(self, parent = None):
        return len(self.playlists)

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        return self.playlists[index.row()]


class library_model(QAbstractListModel):
    """This class will represent the whole library as a list"""
    def __init__(self, database, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.database = database
    def rowCount(self, parent):
        return len(self.database)

    def mimeTypes(self):
        return [FILE_TYPE]

    def mimeData(self, indexes):
        mime_data = QMimeData()
        data = [self.data(x, Qt.DisplayRole) for x in indexes if x.isValid()]
        data = "\n".join(data)
        mime_data.setData(FILE_TYPE, data)
        return mime_data

    def flags(self, index):
        default_flags = QAbstractListModel.flags(self, index)
        if index.isValid():
            return default_flags | Qt.ItemIsDragEnabled
        else:
            return default_flags

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        return self.database[index.row()]

class updater(QTimer):
    def __init__(self, parent):
        QTimer.__init__(self, parent)
        self.gui = parent
        self.timeout.connect(self.update)
    def update(self):
        self.gui.update_status()
        mpd_current_song = self.gui.mpd_api.currentsong()
        if self.gui.status['state'] == 'play' and self.gui.current_song != mpd_current_song:
            self.gui.current_song = mpd_current_song
            self.gui.horizontalSlider.setMaximum(int(self.gui.current_song['time']))
            self.gui.horizontalSlider.setValue(0)
            self.gui.playlist.update_current_song(mpd_current_song['pos'])

class gui_client(QMainWindow, Ui_MainWindow):
    def __init__(self, mpd_api, parent=None):
        QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.mpd_api = mpd_api
        self.current_song = self.mpd_api.currentsong()

        self.setup_actions()

        self.setup_library()

        self.setup_playlists()

        self.setup_playlist()

        self.setup_database_songs()

        self.updater = updater(self)
        self.updater.start(1000)
        self.updater.update()

    def setup_actions(self):
        self.actionToggle.triggered.connect(self.toggle_handle)
        self.actionStop.triggered.connect(self.stop_handle)
        self.actionPrev.triggered.connect(self.play_previous)
        self.actionNext.triggered.connect(self.playnext)
        self.actionSave.triggered.connect(self.save_playlist)
        self.actionClear.triggered.connect(self.clear_playlist)
        self.actionLoad_Playlist.triggered.connect(self.load_playlist)
        self.searchDirLib.textEdited.connect(self._filter_dirlib_files)
        self.horizontalSlider.sliderReleased.connect(self.seek)
        self.searchLib.textEdited.connect(self._filter_database_songs)

    def update_status(self):
        self.status = self.mpd_api.status()
        if self.status['state'] == 'play' and self.current_song is not None:
            self.horizontalSlider.setDisabled(False)
            self.actionToggle.setText('Pause')
            self.horizontalSlider.setMaximum(int(self.current_song['time']))
            current_position = self.status['time'].split(":")[0]
            self.horizontalSlider.setValue(int(current_position))
        else:
            self.horizontalSlider.setDisabled(True)
            self.actionToggle.setText('Play')

    def _filter_dirlib_files(self, value):
        if value is None or value == '':
            self.library_dir_model.setNameFilters([])
        else:
            self.library_dir_model.setNameFilters(['*' + value + '*'])

    def _filter_database_songs(self, pattern):
        if pattern is None or pattern == '':
            all_songs_info = [x['file'] for x in self.mpd_api.listallinfo() if 'file' in x]
            self.libraryModel.database = all_songs_info
        else:
            matching_songs = self.mpd_api.search('any', pattern)
            matching_songs = [x['file'] for x in matching_songs]
            self.libraryModel.database = matching_songs
        self.libraryModel.reset()

    def setup_library(self):
        self.library_dir_model = QFileSystemModel(self)
        self.library_dir_model.setReadOnly(False)
        self.library_dir_model.setNameFilterDisables(False)
        index = self.library_dir_model.setRootPath(DEFAULT_LIB_PATH)
        self.treeView.setModel(self.library_dir_model)
        self.treeView.setRootIndex(index)

    def setup_playlist(self):
        self.playlist = playlist_model(self.mpd_api, self)
        self.tableView.setModel(self.playlist)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.activated.connect(self.play_song)

    def get_playlists(self):
        resources = self.mpd_api.lsinfo()
        playlists = [x['playlist'] for x in resources if x is not None and 'playlist' in x]
        return playlists

    def setup_playlists(self):
        self.playlists = playlists_model(self.get_playlists(), self)
        self.listView.setModel(self.playlists)

    def setup_database_songs(self):
        all_songs_info = [x['file'] for x in self.mpd_api.listallinfo() if 'file' in x]
        self.libraryModel = library_model(all_songs_info, self)
        self.libraryDatabase.setModel(self.libraryModel)

    def seek(self):
        self.mpd_api.seekid(self.current_song['id'], self.horizontalSlider.value())

    def play_song(self, index):
        song = self.playlist.get_song(index, Qt.DisplayRole)
        if song is None:
            return
        self.current_song = song
        self.playlist.update_current_song(self.current_song['pos'])
        self.mpd_api.playid(self.current_song['id'])

    def stop_handle(self):
        self.mpd_api.stop()
        self.horizontalSlider.setValue(0)
        self.playlist.update_current_song(-1)
        self.updater.update()

    def clear_playlist(self):
        self.mpd_api.clear()
        self.playlist.playlistinfo = []
        self.playlist.reset()


    def save_playlist(self):
        playlist_name , ok = QInputDialog.getText(self, "Playlist name", 
                "Playlist name", QLineEdit.Normal)
        if ok and playlist_name:
            self.mpd_api.save(playlist_name)
            self.setup_playlists()
            self.playlists.reset()

    def load_playlist(self):
        playlist_name, ok = QInputDialog.getItem(self, 'Playlist name', 'Playlist name',
                self.get_playlists())
        if ok and playlist_name:
            self.mpd_api.load(playlist_name)
            self.setup_playlist()
            self.playlist.reset()

    def playnext(self):
        self.mpd_api.next()
        self.updater.update()

    def play_previous(self):
        self.mpd_api.previous()
        self.updater.update()

    def select_song(self, song_position):
            index = self.playlist.index(song_position, 0)
            selection_model = self.tableView.selectionModel()
            selection_model.select(index, QItemSelectionModel.ClearAndSelect
                                   | QItemSelectionModel.Rows)

    def toggle_handle(self):
        if 'Play' == self.actionToggle.text():
            self.mpd_api.play()
            self.playlist.update_current_song(self.current_song['pos'])
        else:
            self.playlist.update_current_song(-1)
            self.mpd_api.pause()
        self.updater.update()
