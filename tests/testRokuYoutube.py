import sys
from os import path

sys.path.insert(0, path.dirname(sys.path[0]))

from libs.roku import RokuController

roku = RokuController()

roku.playYoutube('GcHfqtEg3pM')

