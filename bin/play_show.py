import sys
from os import path
from pprint import pprint

sys.path.insert(0, path.dirname(sys.path[0]))

from libs.player import PlayerController

player = PlayerController()

if(len(sys.argv) != 2):
    print("Missing argument, the show to play")
    sys.exit(-1)

show = sys.argv[1]

player.playShow(show)
