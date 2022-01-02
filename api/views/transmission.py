from django.views import View
from django.http import HttpResponse
from django_q.tasks import async_task
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import json

from transmission_rpc import Client

from libs.player import PlayerController

from automommy import secrets

@method_decorator(csrf_exempt, name='dispatch')
class Transmission(View):

    def get(self, request, torrent_id=None, *args, **kwargs):
        if torrent_id == None:
            async_task('subprocess.call', [secrets.transmission_sync_script])
        else:
            async_task('subprocess.call', [secrets.transmission_sync_script, torrent_id])
            
        return HttpResponse()
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        torrent = data["torrent"]
        print(torrent)
        
        c = Client(host=secrets.transmission_endpoint, port=443, username=secrets.transmission_username, password=secrets.transmission_password)

        c.add_torrent(torrent)

        return HttpResponse()
    
