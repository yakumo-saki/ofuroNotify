# -*- coding: utf-8 -*-

from logging import getLogger
logger = getLogger(__name__)

from main.postBase import PostBase

import json
import os
import requests

class WebhookPost(PostBase):

    webhook_url = ""

    def __init__(self):
        super().__init__()

        self.webhook_url = os.environ.get('WEBHOOK_URL')

    def post(self, inOut, lastIn, duration_sec, clicktype, dryrun = False):

        logger.debug(f'start post')

        if (not self.webhook_url):
            logger.debug("no url . skip")
            return

        logger.debug(f'post webhook {self.webhook_url} {inOut} {lastIn} {duration_sec}')

        payload = {'type': f'bath{inOut}', 'duration_sec': duration_sec}

        if dryrun == False:
            r = requests.post(self.webhook_url, data=payload, timeout=2)
        else:
            payload_dump = json.dumps(payload, ensure_ascii=False)
            logger.debug(f'self.webhook_url payload={payload_dump}')

        logger.debug('done')
