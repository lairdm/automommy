from django_sns_view.views import SNSEndpoint
from django_q.tasks import async_task

from libs.player import PlayerController

from automommy import secrets

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
        elif command['action'] == 'sync':
            if 'torrent_id' in command:
                async_task('subprocess.call', [secrets.transmission_sync_script, command['torrent_id']])
            else:
                async_task('subprocess.call', [secrets.transmission_sync_script])
