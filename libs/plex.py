from plexapi.server import PlexServer
from plexapi import utils

from automommy import secrets

class PlexController():
    
    plex = None
    plexClient = None
    plexLibrary = None
    
    def __init__(self):
        self.plex = PlexServer(secrets.plexBaseUrl, secrets.token)
        self.plexLibrary = self.plex.library.section(secrets.librarySection)

    def initializeRoku(self):
        self.plexClient = self.plex.client(secrets.rokuClientName)

    def printClients(self):
        print("Available plex clients:")
        for client in self.plex.clients():
            print(client.title)

    # Get a show by name
    def getShow(self, showName):
        shows = self.plexLibrary.search(title=showName)

        # We're just going to return the first
        if shows:
            return shows[0]

        return None

    def getEpisodeCount(self, showName):
        show = self.getShow(showName)

        return len(show.episodes()) if show else None

    def getUnwatchedEpisodeCount(self, showName):
        show = self.getShow(showName)

        return len(list(filter(lambda x: not x.isWatched, show.episodes())))
            
    def getNextEpisode(self, showName):
        show = self.getShow(showName)

        for episode in show.episodes():
            if episode.isWatched:
                continue

            return episode

        return None

    def playEpisode(self, episode):
        self.plexClient.playMedia(episode)
        
    def resetWatched(self, showName):
        show = self.getShow(showName)

        for episode in show.episodes():
            episode.markUnwatched()


