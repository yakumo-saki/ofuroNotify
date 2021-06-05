# -*- coding: utf-8 -*-

import boto3
from boto3.session import Session
from concurrent import futures
from main.main import main_process

import logging
import logging.config
import yaml

import json

import os
import subprocess

class JsonFormatter:
    def format(self, record):
        return json.dumps(vars(record))

# lambda から呼び出されたときのエントリポイント
# ローカル環境でのテスト時は lambda_debug_entrypoint.pyがエントリポイント
def lambda_handler(event, context):

    # logging.config.dictConfig(yaml.safe_load(open("logging.yaml").read()))

    logging.basicConfig() # 標準エラーに出力するハンドラーをセット
    logging.getLogger().handlers[0].setFormatter(JsonFormatter()) # ハンドラーの出力フォーマットを自作のものに変更

    # 以降は普通にloggerを取得して処理を関数を書く
    logger = logging.getLogger(__name__)
    logger.setLevel(os.environ.getenv('LOG_LEVEL', 'INFO'))

    dynamodb = boto3.resource('dynamodb')

    type = main_process(dynamodb, event, context)

    return {
        'statusCode': 200,
        'status': 'success',
        'type' : type
    }

