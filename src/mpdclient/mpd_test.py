#!/usr/bin/env python3.1
# -*- coding: utf-8 -*-

# IMPORTS
from mpd import (MPDClient, CommandError)
from random import choice
from socket import error as SocketError
from sys import exit
import sys
import os


## SETTINGS
##
HOST = 'localhost'
PORT = '6600'
PASSWORD = False
MUSIC_LIB= '/var/lib/mpd/music'
###


client = MPDClient()

try:
    client.connect(host=HOST, port=PORT)
except SocketError:
    exit(1)

if PASSWORD:
    try:
        client.password(PASSWORD)
    except CommandError:
        exit(1)
function = getattr(client, sys.argv[1])
if len(sys.argv[2:]) > 0:
    print(function(*sys.argv[2:]))
else:
    print(function())


#file_to_delete = os.path.join(MUSIC_LIB, client.currentsong()['file'])
#os.remove(file_to_delete)


# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab
