import boto3
from boto3.session import Session
from concurrent import futures

import os
import time
import json
import random

import slackweb
from mastodon import Mastodon


dynamodb = None


# 処理のメイン部分
def main_process(aDynamodb, event, context):
    dynamodb = aDynamodb

    params = get_params_from_env()

    if (len(params) == 0):
        raise ValueError("no env params")

    message = 'test ' + str(random.randint(2, 1000)) + ' num'

    future_list = []
    with futures.ThreadPoolExecutor(max_workers=4) as executor:

        for param in params:
            if param["type"] == 'mastodon':
                mastodon = executor.submit(fn=mastodon_post, message=message, url=param["url"], token=param["token"])
                future_list.append(mastodon)
            elif param["type"] == 'slack':
                slack = executor.submit(fn=slack_post, message=message, webhook=param["url"])
                future_list.append(slack)
            else:
                raise ValueError("unknown type {param['type']}")

    _ = futures.as_completed(fs=future_list)

    print('completed.')


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


def slack_post(message, webhook):
    print(f'slack post msg {message} webhook url {webhook}')
    slack = slackweb.Slack(url=webhook)
    slack.notify(text=message)
    print('slack done')


def twitter_post(message, webhook):
    print(f'twitter post msg {message} webhook url {webhook}')
    sleep_seconds = random.randint(2, 4)
    time.sleep(sleep_seconds)


def mastodon_post(message, url, token):
    print(f'mastodon post msg {message} webhook url {url} token {token}')
    mastodon = Mastodon(access_token = token, api_base_url = url)
    mastodon.toot(message + " 👁️")
    print('mastodon done')
