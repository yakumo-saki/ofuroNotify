# -*- coding: utf-8 -*-

# まだこのモジュールは未完成

import configparser
import boto3
import json
import os
from logging import getLogger

logger = None

def sqs_main(*, specificLogger=None):

    logger = getLogger(__name__)
    sqs = boto3.client('sqs')

    logger = specificLogger or logger

    logger.debug(f"sqs_main start")

    url = os.environ.get("SQS_ENDPOINT")

    # 送信するJSON
    body = {"type": "Right", "Action": "On"}

    logger.debug(f"send message {body}")

    # SQSへJSONの送信
    response = sqs.send_message(
        QueueUrl=url,
        DelaySeconds=0,
        MessageBody=(
            json.dumps(body)
        )
    )

    logger.debug(f'sent message. result = {response}')

    # logger.debug(f"receive message")
    # SQSからJSONを受信
    # response = sqs.receive_message(
    #     QueueUrl=url,
    #     AttributeNames=[
    #         'SentTimestamp'
    #     ],
    #     MaxNumberOfMessages=1,
    #     VisibilityTimeout=0,
    #     WaitTimeSeconds=0
    # )

    # message = response['Messages'][0]
    # body = json.loads(message['Body'])
    # logger.debug(f"got message {body}")

    # メッセージを削除するための情報を取得
    # receipt_handle = message['ReceiptHandle']

    # メッセージを削除
    # sqs.delete_message(
    #     QueueUrl=url,
    #     ReceiptHandle=receipt_handle
    # )
    #
    #logger.debug(f"deleted {receipt_handle}")
