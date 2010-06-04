'''
Created on May 27, 2010

@author: nikolavp
'''
HOST = "localhost"
PORT = "6600"
PASSWORD = None
from GuiClient import GuiClient
from PyQt4.QtGui import QApplication
from mpd import *
from socket import error as SocketError
import logging
import sys

def connect():
    mpd_api = MPDClient()
    try:
        mpd_api.connect(host=HOST, port=PORT)
    except SocketError:
        log.error("Couldn't connect to %s on port %s" % (HOST, PORT))
        exit(1)
    
    if PASSWORD:
        try:
            mpd_api.password(PASSWORD)
        except CommandError:
            log.error("Couldn't authenticate to %s on port %s" % (HOST, PORT))
            exit(1)
    return mpd_api

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    log = logging.getLogger("mpd")
    mpd_api = connect();

    app = QApplication(sys.argv)
    gui = GuiClient(mpd_api)
    gui.show()
    app.exec_() 
