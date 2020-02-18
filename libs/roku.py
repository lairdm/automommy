from roku import Roku
import requests

from automommy import secrets

class RokuController():

    plexAppName = 'Plex - Stream Free TV & Movies'
    youtubeAppName = 'YouTube'

    youtubeUri = 'http://{rokuIp}:8060/launch/837?contentId={videoId}&mediaType=live'

    roku = None

    def __init__(self):
        self.roku = Roku(secrets.rokuIP)

    def home(self):
        roku.home()
        
    def launchPlex(self):
        plex = self.roku[self.plexAppName]
        plex.launch()

    def playPlex(self, videoId):
        plex = self.roku[self.plexAppName]
        self.roku.launch(plex, params={'contentId':videoId, 'mediaType':'live'})
        
    def playYoutube(self, videoId):
        youtube = self.roku[self.youtubeAppName]
        self.roku.launch(youtube, params={'contentId':videoId, 'mediaType':'live'})
#        uri = self.youtubeUri.format(rokuIp=self.rokuIP, videoId=videoId)
#        requests.post(url = uri)
        
