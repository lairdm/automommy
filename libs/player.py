
from .plex import PlexController
from .roku import RokuController
from .database import DatabaseController

from pprint import pprint
import time

"""
Player controller for episodes
"""
class PlayerController():

    def __init__(self):
        self.plex = PlexController()
        self.roku = RokuController()
        self.database = DatabaseController()

    """
    Play a show by name (slug in the database)
    """
    def playShow(self, showName):
        show = self.database.fetchShow(showName)
        pprint(vars(show))
            
        if not show:
            print("We have an error, show {0} not found".format(showName))
            return

        showPlaying = False
        
        if show.lastshown == -1 and show.plexname:
            # Off to plex
            # Try to play from plex
            showPlaying = self.playViaPlex(show)

        if (not showPlaying) and show.hasexternal:
            print("Attempting to play via external player")
            episode = self.database.fetchNextEpisode(show)

            if episode.linktype == 'youtube':
                print("Playing via youtube ({0})".format(episode.uri))
                self.roku.playYoutube(episode.uri)
                return

            print("If we're here, we haven't played anything")

    """
    If a show is from plex, try to play is via plex and rewind the
    watched counter if needed

    Return True if we played an episode and False if we didn't
    (either didn't find one or rewound the watched counter)
    """
    def playViaPlex(self, show):
        print("Playing {0} via plex".format(show.plexname))
        plexShow = self.plex.getShow(show.plexname)

        if not plexShow:
            print("Odd, we can't find this show in plex")
            return False

        remaining = self.plex.getUnwatchedEpisodeCount(show.plexname)

        if remaining <= 0:
            print("No episodes left in plex, resetting count")
            self.plex.resetWatched(show.plexname)
            
            if show.hasexternal:
                return False
        else:
            print("{0} episodes left in plex".format(remaining))

        nextEpisode = self.plex.getNextEpisode(show.plexname)

        print("Attempting to play via plex")
#        episodeid = nextEpisode.key
        episodeid = nextEpisode.guid
#        episodeid = nextEpisode.getStreamURL()
#        self.roku.playPlex(episodeid)
        print("Playing: {0}".format(nextEpisode.title))
        print("Ratingkey: {0}".format(episodeid))
#        return
        self.roku.launchPlex()
        # Wait for plex to launch
        time.sleep(7)
        self.plex.printClients()
        self.plex.initializeRoku()
        self.plex.playEpisode(nextEpisode)

        return True

