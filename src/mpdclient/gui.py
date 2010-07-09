'''
Created on May 28, 2010
@author: nikolavp
'''

from PyQt4.Qt import Qt
from PyQt4.Qt import QAbstractListModel, Qt, QMainWindow, QFileSystemModel, \
    QAbstractTableModel, QAbstractItemView, QItemSelectionModel, QTimer, \
    QMouseEvent, QMimeData, QDataStream, QIODevice, QPalette
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
        self.playlistinfo = mpd_api.playlistinfo()
        self.header_data = PLAYLIST_HEADER_DATA
        self.current_song_pos = -1
    
    def flags(self, index):
        default_flags = QAbstractTableModel.flags(self, index)
        if(index.isValid()):
            return default_flags | Qt.ItemIsDropEnabled
        else:
            return default_flags | Qt.ItemIsDropEnabled
    
    def update_current_song(self, pos):
        self.current_song_pos = pos
        
    def insertRows(self, row, count, parent = None):
        self.playlistinfo[row:row] = [None] * count
    
    def mimeTypes(self):
        return [FILE_TYPE]
        
    def dropMimeData(self, data, action, row, column, parent = None):
        if (action == Qt.IgnoreAction):
            return True;
        
        if not data.hasFormat(FILE_TYPE):
            return False;
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
        
    def setData(self, index, val, parent = None):
        #We only care about the rows
        self.playlistinfo[index.row()] = val
        
    
#    def mimeData(self, indexes):
#        print("bla")
#        mime_data = QMimeData()
#        encoded_data = None
#        QDataStream.stream(encoded_data, QIODevice.WriteOnly)
        
    def rowCount(self, parent):
        return len(self.playlistinfo)

    def columnCount(self, parent):
        return len(self.header_data)

    def get_song(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        return self.playlistinfo[index.row()]
    
    def modify_field(self, field, value):
        if field == 'time':
            seconds = int(value)
            if seconds > 60:
                return str(seconds // 60) + ":" + str(seconds % 60)
            else:
                return seconds
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
        return None

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

    def supportedDragActions(self):
        return Qt.CopyAction | Qt.MoveAction

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
        if(index.isValid()):
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
        if self.gui.current_song != mpd_current_song:
            self.gui.current_song = mpd_current_song
            self.gui.horizontalSlider.setMaximum(int(self.gui.current_song['time']))
            self.gui.horizontalSlider.setValue(0)
            pos = int(mpd_current_song['pos'])
            self.gui.playlist.update_current_song(pos)
        
class gui_client(QMainWindow, Ui_MainWindow):
    def update_status(self):
        self.status = self.mpd_api.status()
        if self.status['state'] == 'play' and self.current_song is not None:
            self.horizontalSlider.setDisabled(False)
            self.actionToggle.setText('Pause')
            self.horizontalSlider.setMaximum(int(self.current_song['time']))
            current_position = self.mpd_api.status()['time'].split(":")[0]
            self.horizontalSlider.setValue(int(current_position))
        else:
            self.horizontalSlider.setDisabled(True)
            self.actionToggle.setText('Play')
      
    def __init__(self, mpd_api, parent=None):
        QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.mpd_api = mpd_api
        self.current_song = self.mpd_api.currentsong()

        self.actionToggle.triggered.connect(self.toggle_handle)
        self.actionStop.triggered.connect(self.stop_handle)
        self.actionPrev.triggered.connect(self.play_previous)
        self.actionNext.triggered.connect(self.playnext)
        self.searchDirLib.textEdited.connect(self._filter_dirlib_files)
        
        self.horizontalSlider.sliderReleased.connect(self.seek)
        self.searchLib.textEdited.connect(self.setup_database_songs)

        self.libraryDirModel = QFileSystemModel(self)
        self.libraryDirModel.setReadOnly(False)
        self.libraryDirModel.setNameFilterDisables(False)
        #TODO: This is using a hardcoded string that should 
        #be changeable in other releases
        index = self.libraryDirModel.setRootPath(DEFAULT_LIB_PATH)
        self.treeView.setModel(self.libraryDirModel)
        self.treeView.setRootIndex(index)

        self.setup_playlists()

        self.playlist = playlist_model(mpd_api, self)
        self.tableView.setModel(self.playlist)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.activated.connect(self.play_song)

        self.setup_database_songs(None)

        self.updater = updater(self)
        self.updater.start(1000)
        self.updater.update()

    def _filter_dirlib_files(self, value):
        if value is None or value == '':
            self.libraryDirModel.setNameFilters([])
        else:
            self.libraryDirModel.setNameFilters(['*' + value + '*'])

    def setup_database_songs(self, pattern):
        if pattern is None or pattern == '':
            all_songs_info = [x['file'] for x in self.mpd_api.listallinfo() if 'file' in x]
            self.libraryModel = library_model(all_songs_info, self)
        else:
            matching_songs = self.mpd_api.search('any', pattern)
            matching_songs = [x['file'] for x in matching_songs]
            self.libraryModel = library_model(matching_songs, self)
        self.libraryDatabase.setModel(self.libraryModel)

    def seek(self):
        self.mpd_api.seekid(self.current_song['id'], self.horizontalSlider.value())
    
    def play_song(self, index):
        song = self.playlist.get_song(index, Qt.DisplayRole)
        self.mpd_api.playid(song['id'])
        self.current_song = song

    def setup_playlists(self):
        resources = self.mpd_api.lsinfo()
        playlists = [x['playlist'] for x in resources if x is not None and 'playlist' in x]
        self.playlists = playlists_model(playlists, self)
        self.listView.setModel(self.playlists)

    def stop_handle(self):
        self.mpd_api.stop()
        self.updater.update()
        
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
            self.select_song(int(self.current_song['pos']))
        else:
            self.mpd_api.pause()
        self.updater.update()

