#!/usr/bin/env python3.1
# vim: set sw=4 sts=4 et foldmethod=indent :

from PyQt4.QtGui import QAction, QApplication
from gui import gui_client
from mpd import MPDClient
import sys
import unittest

class gui_client_test(unittest.TestCase):
    def __init__(self, name):
        unittest.TestCase.__init__(self, name)

    def setUp(self):
        mpd_api = MPDClient()
        mpd_api.connect("localhost", 6600)
        self.gui = gui_client(mpd_api)

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
