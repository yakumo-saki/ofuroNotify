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


    def post(self, inOut, lastIn, duration_sec, clicktype, dryrun = False):

        logger.debug(f'start post')

        if (not self.mastodon_url or not self.mastodon_token):
            logger.debug("no url or token. skip")
            return

        message = self.create_message(inOut, lastIn, duration_sec, clicktype)

        logger.debug(f'post msg {message} url {self.mastodon_url}')

        mastodon = Mastodon(access_token = self.mastodon_token, api_base_url = self.mastodon_url)

        if dryrun == False:
            mastodon.toot(message + " 👁️")

        logger.debug('done')
