#!/usr/bin/env python3.1
# vim: set sw=4 sts=4 et foldmethod=indent :

from PyQt4.QtGui import QAction, QApplication
from PyQt4.QtCore import Qt
from gui import gui_client, playlist_model, library_model, playlists_model, PLAYLIST_HEADER_DATA
from mpd import MPDClient
import sys
import unittest

#A playlist that tests for most of the stuff like null values and so on
#This will be reused so it is defined as global
testing_playlist = [{'title': 'Foo', 'artist': 'Bar', 'pos': '0', 'file': 'Foo - Bar', 'time': '216', 'date': '2010', 'id': '0'},
                                 {'album': 'org.nikolavp', 'performer': 'org.nikolavp', 'composer': None, 'title': 'Life sucks', 'artist': 'Nikolavp', 'pos': '1', 'genre': 'Rock', 'albumartist': 'Nikolavp', 'file': None, 'time': '297', 'date': '2010-06-26', 'id': '1'}, ]


class playlist_model_test(unittest.TestCase):
    def setUp(self):
        self.model = playlist_model(testing_playlist)
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

    def test_get_row(self):
        test_general = self.model.get_song(self.first_row, Qt.DisplayRole)
        self.assertTrue('Bar' in test_general.values())
        self.assertTrue('Foo' in test_general.values())
        test_nulls = self.model.get_song(self.second_row, Qt.DisplayRole)
        self.assertTrue('Nikolavp' in test_nulls.values())
        
        
class playlists_model_test(unittest.TestCase):
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
    def setUp(self):
        mpd_api = MPDClient()
        mpd_api.connect("localhost", 6600)
        self.gui = gui_client(mpd_api)

    def test_getting_playlists(self):
        resources = testing_playlist + [{"playlist" : "Genius"}, {"playlist" : "Second"}, {"playlist" :None}]
        playlists = self.gui._get_playlists(resources)
        self.assertEquals(3, len(playlists))
        self.assertTrue('Genius' in playlists)
        self.assertTrue('Second' in playlists)
        
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
