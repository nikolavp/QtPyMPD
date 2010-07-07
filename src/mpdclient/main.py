#!/usr/bin/env python3.1
'''
Created on May 27, 2010

@author: nikolavp
'''

from gui import gui_client
from PyQt4.QtGui import QApplication
from mpd import MPDClient, CommandError
from socket import error as SocketError
import logging
import sys

HOST = "localhost"
PORT = "6600"
PASSWORD = None

logging.basicConfig(level=logging.WARNING)
LOG = logging.getLogger("mpd")
def connect():
    mpd_api = MPDClient()
    try:
        mpd_api.connect(host=HOST, port=PORT)
    except SocketError:
        LOG.error("Couldn't connect to %s on port %s" % (HOST, PORT))
        exit(1)

    if PASSWORD:
        try:
            mpd_api.password(PASSWORD)
        except CommandError:
            LOG.error("Couldn't authenticate to %s on port %s" % (HOST, PORT))
            exit(1)
    return mpd_api

def main():
    mpd_api = connect()
    mpd_api.update()
    app = QApplication(sys.argv)
    gui = gui_client(mpd_api)
    gui.show()
    app.exec_()
    mpd_api.disconnect()


if __name__ == '__main__':
    main()
