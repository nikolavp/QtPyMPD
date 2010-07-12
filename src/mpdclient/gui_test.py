#!/usr/bin/env python3.1
# vim: set sw=4 sts=4 et foldmethod=indent :

from PyQt4.QtGui import QAction, QApplication
from PyQt4.QtCore import Qt
from gui import gui_client, playlist_model, library_model, playlists_model, PLAYLIST_HEADER_DATA
from mpd import MPDClient
import sys
import unittest



#This mock is created with mpd_test.py for the given function. Try mpd_test.py status
STATUS_PAUSE = {'songid': '0', 'playlistlength': '4', 'playlist': '2', 'repeat': '0', 'consume': '0', 'song': '0', 'random': '0', 'state': 'pause', 'xfade': '0', 'volume': '96', 'single': '0', 'nextsong': '1', 'time': '0:297', 'audio': '44100:24:2', 'bitrate': '0', 'nextsongid': '1'}
STATUS_STOP = {'songid': '1', 'playlistlength': '4', 'playlist': '2', 'repeat': '0', 'consume': '0', 'song': '1', 'random': '0', 'state': 'stop', 'xfade': '0', 'volume': '96', 'single': '0', 'nextsong': '2', 'nextsongid': '2'}
STATUS_PLAY = {'songid': '1', 'playlistlength': '4', 'playlist': '2', 'repeat': '0', 'consume': '0', 'song': '1', 'random': '0', 'state': 'play', 'xfade': '0', 'volume': '96', 'single': '0', 'nextsong': '2', 'time': '3:297', 'audio': '44100:24:2', 'bitrate': '160', 'nextsongid': '2'}
class mpd_mocking_class(object):
    def __init__(self):
        self.status_holder = STATUS_PAUSE
    def playlistinfo(self):
        return [{'title': 'Foo', 'artist': 'Bar', 'pos': '0', 'file': 'Foo - Bar', 'time': '216', 'date': '2010', 'id': '0'},
                                 {'album': 'org.nikolavp', 'performer': 'org.nikolavp', 'composer': None, 'title': 'Life sucks', 'artist': 'Nikolavp', 'pos': '1', 'genre': 'Rock', 'albumartist': 'Nikolavp', 'file': None, 'time': '297', 'date': '2010-06-26', 'id': '1'}, ]
    def lsinfo(self):
        return [{'date': '2009', 'title': 'Chica Bomb ~VILA~', 'artist': 'Dan Balan', 'file': 'Dan Balan - Chica Bomb.mp3', 'time': '216'}, {'album': 'www.Bizonio.Data.Bg', 'performer': 'www.Bizonio.Data.Bg', 'composer': 'www.Bizonio.Data.Bg', 'title': 'Pronto', 'artist': 'Snoop Dogg feat. Soulja Boy', 'genre': 'www.Bizonio.Data.Bg', 'albumartist': 'Snoop Dogg', 'file': 'Snoop Dogg feat. Soulja Boy - Pronto.mp3', 'time': '297', 'date': 'www.-12-08'}, {'last-modified': '2010-07-10T11:48:18Z', 'playlist': 'NEw'}, {'last-modified': '2010-07-10T11:40:15Z', 'playlist': 'llll'}, {'last-modified': '2010-07-10T14:16:46Z', 'playlist': 'Geri'}, {'last-modified': '2010-06-26T15:14:19Z', 'playlist': 'Goodies'}, {'last-modified': '2010-07-06T16:50:44Z', 'playlist': 'playlist'}, {'last-modified': '2010-07-10T11:48:11Z', 'playlist': 'New_Python_Proba'}]
    def currentsong(self):
        return {'album': 'www.Bizonio.Data.Bg', 'performer': 'www.Bizonio.Data.Bg', 'composer': 'www.Bizonio.Data.Bg', 'title': 'Pronto', 'artist': 'Snoop Dogg feat. Soulja Boy', 'pos': '0', 'genre': 'www.Bizonio.Data.Bg', 'albumartist': 'Snoop Dogg', 'file': 'Snoop Dogg feat. Soulja Boy - Pronto.mp3', 'time': '297', 'date': 'www.-12-08', 'id': '0'}
    def listallinfo(self):
        return [{'date': '2009', 'title': 'Chica Bomb ~VILA~', 'artist': 'Dan Balan', 'file': 'Dan Balan - Chica Bomb.mp3', 'time': '216'}, {'album': 'www.Bizonio.Data.Bg', 'performer': 'www.Bizonio.Data.Bg', 'composer': 'www.Bizonio.Data.Bg', 'title': 'Pronto', 'artist': 'Snoop Dogg feat. Soulja Boy', 'genre': 'www.Bizonio.Data.Bg', 'albumartist': 'Snoop Dogg', 'file': 'Snoop Dogg feat. Soulja Boy - Pronto.mp3', 'time': '297', 'date': 'www.-12-08'}]
    def status(self):
        return self.status_holder
    #For the motions with the server we just set the appropriate status
    def play(self):
        self.status_holder = STATUS_PLAY
    def pause(self):
        self.status_holder = STATUS_PAUSE
    def stop(self):
        self.status_holder = STATUS_STOP
#A single instance of the mock
mpd_mock = mpd_mocking_class()

class playlist_model_test(unittest.TestCase):
    """This class is used to test the playlist_model class from the gui module"""
    def setUp(self):
        self.model = playlist_model(mpd_mock)
        self.first_row = self.model.createIndex(0, PLAYLIST_HEADER_DATA.index('Title'))
        self.second_row = self.model.createIndex(1, PLAYLIST_HEADER_DATA.index('Title'))

    def test_proper_model_size(self):
        self.assertEquals(2, self.model.rowCount(None))
        self.assertEquals(6, self.model.columnCount(None))

    def test_data_accesor(self):
        testing_data = self.model.data(self.second_row, Qt.DisplayRole)
        self.assertEquals('Life sucks', testing_data)
        check_null_data = self.model.data(self.second_row, Qt.DecorationRole)
        self.assertIsNone(check_null_data)

    def test_time_data(self):
        self.time_index = self.model.createIndex(0, PLAYLIST_HEADER_DATA.index('Time'))
        time = self.model.data(self.time_index, Qt.DisplayRole)
        self.assertEquals("3:36", time)

    def test_get_song(self):
        test_general = self.model.get_song(self.first_row, Qt.DisplayRole)
        self.assertTrue('Bar' in test_general.values())
        self.assertTrue('Foo' in test_general.values())
        test_nulls = self.model.get_song(self.second_row, Qt.DisplayRole)
        self.assertTrue('Nikolavp' in test_nulls.values())

    def test_modify_field(self):
        more_than_minute = seconds = self.model.modify_field('time', '480')
        self.assertEquals('8:0', more_than_minute)
        less_than_minute = self.model.modify_field('time', '30')
        self.assertEquals('30', less_than_minute)

    def test_insert_rows(self):
        self.assertEquals(2, self.model.rowCount())
        self.model.insertRows(1, 4)
        self.assertEquals(6, self.model.rowCount())

class playlists_model_test(unittest.TestCase):
    """A class to test the playlists_model from the gui module"""
    def setUp(self):
        self.testing_playlists = ["First", "Second",
                                      "Dummy", "FOO", "BAR"]
        self.model = playlists_model(self.testing_playlists)

    def test_row_count(self):
        self.assertEquals(5, self.model.rowCount(None))

    def test_data_returned(self):
        indexes = [self.model.createIndex(x, 0) for x in range(5)]
        results = [self.model.data(index, Qt.DisplayRole) for index in indexes]
        self.assertEquals(self.testing_playlists, results)

class library_model_test(unittest.TestCase):
    """A class to test the library_model from the gui module"""
    def setUp(self):
        self.testing_database_list = ["Foo", "Bar", None]
        self.model = library_model(self.testing_database_list)

    def test_row_count(self):
        self.assertEquals(len(self.testing_database_list),
                      self.model.rowCount(None))

    def test_data_returned(self):
        indexes = [self.model.createIndex(x, 0) for x in range(3)]
        results = [self.model.data(index, Qt.DisplayRole) for index in indexes]
        self.assertEquals(self.testing_database_list, results)

class gui_client_test(unittest.TestCase):
    """A TestCase for the methods in the gui_client class from the gui module"""
    def setUp(self):
        self.gui = gui_client(mpd_mock)

    def test_getting_playlists(self):
        playlists = self.gui.playlists.playlists
        self.assertEquals(len(playlists), self.gui.playlists.rowCount())
        self.assertTrue('Goodies' in playlists)
        self.assertTrue('New_Python_Proba' in playlists)

    def test_toggle_text_change_on_different_events(self):
        self.gui.actionStop.activate(QAction.Trigger)
        self.assertEquals('Play', self.gui.actionToggle.text())
        self.gui.actionToggle.activate(QAction.Trigger)
        self.assertEquals('Pause', self.gui.actionToggle.text())
        self.gui.actionToggle.activate(QAction.Trigger)
        self.assertEquals('Play', self.gui.actionToggle.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    unittest.main()
    app._exec()
