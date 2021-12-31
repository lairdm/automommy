from django.views import View
from django.http import HttpResponse

from libs.player import PlayerController

class Launcher(View):

    def get(self, request, show, location, *args, **kwargs):
        player = PlayerController()

        player.playShow(show)

        return HttpResponse()
