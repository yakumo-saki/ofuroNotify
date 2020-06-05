import boto3
from boto3.session import Session
from concurrent import futures

import os
import time
import json
import random

from src.dynamoService import DynamoService
from src.post import *

from datetime import datetime, timedelta
from decimal import *
import math

dynamodb = None

# 処理のメイン部分
def main_process(aDynamodb, event, context):
    dynamodb = aDynamodb

    sns_list = get_params_from_env()

    if (len(sns_list) == 0):
        raise ValueError("no env params")

    # determin In or Out
    dynamo = DynamoService(dynamodb)
    dynamo.setup_tables()
    last_history = dynamo.get_last_history()

    #
    inOut = "In"
    lastIn = None
    duration = None
    print(last_history)
    if last_history == None:
        pass
    elif last_history["InOut"] == 'In':
        inOut = "Out"
        lastIn = last_history["UnixTime"]
        duration_sec = Decimal(math.floor(datetime.now().timestamp())) - lastIn
        duration = duration_to_text(duration_sec)
    else:
        pass

    #print(f'params {inOut} {lastIn}')

    if inOut == 'In':
        message = f'おふろる 🛀'
    else:
        message = f'ほかぱい！ ✨ ({duration})'

    dynamo.put_history(inOut, lastIn)

    post_sns(sns_list, message)


def duration_to_text(second):
    delta = timedelta(seconds=int(second) )

    ret = ""
    if (delta.days > 0):
        ret = f'{delta.days}日'

    m, s = divmod(delta.seconds, 60)
    h, m = divmod(m, 60)

    if (h > 0):
        ret = f'{ret} {h}時間'

    ret = f'{ret} {m}分 {s}秒'

    return ret.strip()

def post_sns(sns_list, message):
    future_list = []
    with futures.ThreadPoolExecutor(max_workers=4) as executor:

        for param in sns_list:
            if param["type"] == 'mastodon':
                mastodon = executor.submit(fn=mastodon_post, message=message, url=param["url"], token=param["token"])
                future_list.append(mastodon)
            elif param["type"] == 'slack':
                slack = executor.submit(fn=slack_post, message=message, webhook=param["url"])
                future_list.append(slack)
            else:
                raise ValueError("unknown type {param['type']}")

    _ = futures.as_completed(fs=future_list)


def get_params_from_env():
    result = []

    # mastodon
    mastodon_url = os.environ.get('MASTODON_URL')
    mastodon_token = os.environ.get('MASTODON_ACC_TOKEN')
    if (mastodon_url and mastodon_token):
        result.append( {"type": 'mastodon', "url": mastodon_url, "token": mastodon_token})

    # slack
    slack = os.environ.get('SLACK_URL')
    if (slack):
        result.append( {"type": 'slack', "url": slack})

    return result


