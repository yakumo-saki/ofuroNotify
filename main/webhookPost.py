# -*- coding: utf-8 -*-

from logging import getLogger
logger = getLogger(__name__)

from main.postBase import PostBase

import json
import os
import requests
from pprint import pprint

class WebhookPost(PostBase):

    webhook_url = ""

    def __init__(self):
        super().__init__()

        self.webhook_url = os.environ.get('WEBHOOK_URL')

    def post(self, inOut, lastIn, duration_sec, clickType, dryrun = False):

        logger.debug(f'start post')

        if (not self.webhook_url):
            logger.debug("no url . skip")
            return {"success": True, "message": "No URL. Webhook post skip."}

        logger.debug(f'post webhook {self.webhook_url} inOut={inOut} lastIn={lastIn} duration={duration_sec}')

        payload = {'type': f'bath{inOut}', 'duration_sec': duration_sec, 'clickType': clickType}

        response = None
        if dryrun == False:
            response = requests.post(self.webhook_url, data=payload, timeout=30)
            logger.info(response.json())
        else:
            payload_dump = json.dumps(payload, ensure_ascii=False)
            logger.info(f'{self.webhook_url} payload={payload_dump}')

        logger.debug('done')
        return {"success": True, "message": "Webhook post ok.", "response": response}
