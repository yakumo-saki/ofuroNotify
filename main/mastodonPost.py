# -*- coding: utf-8 -*-

from logging import getLogger
logger = getLogger(__name__)

from main.postBase import PostBase

import os
from mastodon import Mastodon

class MastodonPost(PostBase):

    webhook_url = ""

    def __init__(self):
        super().__init__()

        self.mastodon_url = os.environ.get('MASTODON_URL')
        self.mastodon_token = os.environ.get('MASTODON_ACC_TOKEN')


    def post(self, inOut, lastIn, duration_sec, clickType, dryrun = False):

        logger.debug(f'start post')

        if (not self.mastodon_url or not self.mastodon_token):
            logger.debug("no url or token. skip")
            return {"success": True, "message": "No URL. Mastodon post skip."}

        message = self.create_message(inOut, lastIn, duration_sec, clickType)

        logger.info(f'post msg {message} url {self.mastodon_url}')

        mastodon = Mastodon(access_token = self.mastodon_token, api_base_url = self.mastodon_url)

        if dryrun == False:
            mastodon.toot(message + " 👁️")

        logger.debug('done')
        return {"success": True, "message": "Mastodon post ok"}
