# -*- coding: utf-8 -*-

import boto3
from boto3.session import Session
from concurrent import futures
from main.main import main_process

import logging
import logging.config

import json
import yaml

import os
import subprocess

logging.config.dictConfig(yaml.safe_load(open("logging-debug.yaml").read()))

# テスト用に直接呼び出ししたとき
if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logger.info("デバッグ実行 NOTIFY")

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', use_ssl=False, endpoint_url="http://localhost:8000",
					aws_access_key_id='local', aws_secret_access_key='local')

    if dynamodb == None:
        logger.error("Cant connect DynamoDB Local")
        exit(16)

    # テストデータを作成
    event = {}
    clickType = {'clickType': 'SINGLE'}
    event["deviceEvent"] = {}
    event["deviceEvent"]['buttonClicked'] = clickType

    type = main_process(dynamodb, event, None)

    logger.info(f"type = {type}")
    logger.info("デバッグ実行 NOTIFY DONE")
