import boto3
from boto3.session import Session
from concurrent import futures
from src.main import main_process

import logging
import logging.config

import json
import yaml

import os
import subprocess


# テスト用に直接呼び出ししたとき
if __name__ == "__main__":
    logging.config.dictConfig(yaml.safe_load(open("logging-debug.yaml").read()))

    logger = logging.getLogger(__name__)
    logger.info("デバッグ実行 NOTIFY")

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', use_ssl=False, endpoint_url="http://localhost:8000",
					aws_access_key_id='local', aws_secret_access_key='local')
    main_process(dynamodb, None, None)
