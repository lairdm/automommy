import sys
from os import path

sys.path.insert(0, path.dirname(sys.path[0]))

from libs.player import PlayerController

player = PlayerController()

player.playShow('misterrogers')
