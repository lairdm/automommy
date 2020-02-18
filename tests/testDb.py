import sys
from os import path
from pprint import pprint

sys.path.insert(0, path.dirname(sys.path[0]))

from libs.database import DatabaseController

database = DatabaseController()

show = database.fetchShow('inthenightgarden')
pprint(vars(show))

show = database.fetchShow('misterrogers')
pprint(vars(show))

nextepisode = database.fetchNextEpisode(show)
if nextepisode:
    print("yes")
    pprint(vars(nextepisode))
else:
    print("off to plex")
