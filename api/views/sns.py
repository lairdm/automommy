from django_sns_view.views import SNSEndpoint

from libs.player import PlayerController

import json
from pprint import pprint

class SNSView(SNSEndpoint):

    def handle_message(self, message, payload):
        # Process the message
        pprint(message)
        pprint(payload)
        command = json.loads(message)

        player = PlayerController()

        if command['action'] == 'play':
            player.playShow(command['show'])
