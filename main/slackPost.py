# -*- coding: utf-8 -*-

from logging import getLogger
logger = getLogger(__name__)

from main.postBase import PostBase

import os
import slackweb

class SlackPost(PostBase):

    def __init__(self):
        super().__init__()

        self.webhook_url = os.environ.get('SLACK_URL')


    def post(self, inOut, lastIn, duration_sec, clickType, dryrun = False):

        logger.debug(f'start post')

        if (not self.webhook_url):
            logger.debug("no url . skip")
            return {"success": True, "message": "No url specified. skip"}

        message = self.create_message(inOut, lastIn, duration_sec, clickType)
        message = "<!channel> " + message

        logger.info(f'post msg {message} webhook url {self.webhook_url}')
        slack = slackweb.Slack(url=self.webhook_url)

        if dryrun == False:
            slack.notify(text=message)

        logger.debug('done')
        return {"success": True, "message": "Slack post ok"}
