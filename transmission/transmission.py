#!/usr/bin/env python

import sys, os
import subprocess
from transmission_rpc import Client
from plexapi.server import PlexServer
from plexapi import utils 

from pprint import pprint

from secrets import *

def getConnection():
    
    c = Client(host=hostname, port=443, username=username, password=password)

    return c

def sync_torrent(torrent_id=None):

    if torrent_id == None:
#        rsync -avP --delete feral:private/deluge/data/* /vol/torrents/
        remote_file = remote_host + ":" + remote_path + "*"

        p = subprocess.Popen(["rsync", "-avP", "--delete", remote_file, local_path])
        sts = os.waitpid(p.pid, 0)
    else:
        connection = getConnection()
        torrent = connection.get_torrent(torrent_id)

        file = torrent.files()[0].name

        # Completely unsafe, get the top level path
        base_path = file.split(os.path.sep)[0]

        remote_file = remote_host + ":" + os.path.join(remote_path, base_path)

        print(remote_file)
        p = subprocess.Popen(["scp", "-Tr", remote_file, local_path])
        sts = os.waitpid(p.pid, 0)


def sync_plex():

    plex = PlexServer(baseurl, token)

    section = plex.library.sectionByID(plex_section_id)
    section.refresh()

if __name__ == "__main__":
    torrent_id = None
    if len(sys.argv) > 1:
        torrent_id = sys.argv[1]

    print(torrent_id)
    sync_torrent(torrent_id)

    sync_plex()
    
