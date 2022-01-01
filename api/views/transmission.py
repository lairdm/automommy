from django.views import View
from django.http import HttpResponse
from django_q.tasks import async_task

from libs.player import PlayerController

from automommy import secrets

class Transmission(View):

    def get(self, request, torrent_id=None, *args, **kwargs):
        if torrent_id == None:
            async_task('subprocess.call', [secrets.transmission_sync_script])
        else:
            async_task('subprocess.call', [secrets.transmission_sync_script, torrent_id])
            
        return HttpResponse()
    
