# -*- coding: utf-8 -*-

from logging import getLogger
logger = getLogger(__name__)

from concurrent import futures

import os

from main.dynamoService import DynamoService
from main.slackPost import SlackPost
from main.mastodonPost import MastodonPost
from main.webhookPost import WebhookPost

from datetime import datetime, timedelta
from decimal import *
import math

dynamodb = None

def get_click_type(event):
    clicktype = event['deviceEvent']['buttonClicked']['clickType']
    print(clicktype)

    if (clicktype == "SINGLE"):
        message = "ボタンが1回押されました"
    elif (clicktype == "DOUBLE"):
        message = "ボタンが2回押されました"
    elif (clicktype == "LONG"):
        message = "ボタンが長押しされました"
    else:
        message = "clickTypeを正常に取得できませんでした"

    return clicktype

# 処理のメイン部分
def main_process(aDynamodb, event, context):

    logger.debug("main_process start")
    dryrun = (os.environ.get('DRYRUN') == "1")

    if dryrun:
        logger.info("DRYRUN")

    clicktype = get_click_type(event)

    dynamodb = aDynamodb

    # determin In or Out
    dynamo = DynamoService(dynamodb)
    dynamo.setup_tables()

    (inOut, lastIn, duration_sec) = get_new_params(dynamo)
    logger.debug(f'got params {inOut} {lastIn} {duration_sec}')

    if not dryrun:
        dynamo.put_history(inOut, lastIn)

    post_sns(inOut, lastIn, duration_sec, clicktype, dryrun)

    logger.debug("main_process done")
    return inOut


def get_new_params(dynamo):
    # お風呂入るの設定
    inOut = "In"
    lastIn = None
    duration = None
    duration_sec = None

    last_history = dynamo.get_last_history()

    if last_history == None:
        pass
    elif last_history["InOut"] == 'In':
        inOut = "Out"
        lastIn = last_history["UnixTime"]
        duration_sec = Decimal(math.floor(datetime.now().timestamp())) - lastIn
    else:
        pass

    return inOut, lastIn, duration_sec


def post_sns(inOut, lastIn, duration_sec, clickType, dryrun = False):
    future_list = []
    with futures.ThreadPoolExecutor(max_workers=10) as executor:

        params = {'inOut': inOut, 'lastIn': 'lastIn', 'duration_sec': duration_sec, 'clickType': clickType, 'dryrun': dryrun}

        mastodon_post = MastodonPost()
        mastodon = executor.submit(fn=mastodon_post.post, **params)
        future_list.append(mastodon)

        slack_post = SlackPost()
        slack = executor.submit(fn=slack_post.post, **params)
        future_list.append(slack)

        webhook_post = WebhookPost()
        webhook = executor.submit(fn=webhook_post.post, **params)
        future_list.append(webhook)

    _ = futures.as_completed(fs=future_list)
