#!/usr/bin/env python3.1
# vim: set sw=4 sts=4 et foldmethod=indent :

import unittest
import sys
from mpd import MPDClient
from gui import gui_client
from PyQt4.QtGui import QApplication

class gui_client_test(unittest.TestCase):

    def __init__(self, name):
        unittest.TestCase.__init__(self, name)
        self.app = QApplication(sys.argv)

    def setUp(self):
        mpd_api = MPDClient()
        mpd_api.connect("localhost", 6600)
        self.gui = gui_client(mpd_api)

    def testToggleButtonTextUpdate(self):
        self.assertEquals("Play", self.gui.actionToggle.text())

if __name__ == '__main__':
    unittest.main()
    app._exec()
