import boto3
from boto3.session import Session
from concurrent import futures
from src.sqs import sqs_main

import logging
import logging.config
import yaml

import json

import os
import subprocess


# テスト用に直接呼び出ししたとき
if __name__ == "__main__":

    logging.config.dictConfig(yaml.safe_load(open("logging-debug.yaml").read()))

    logger = logging.getLogger(__name__)
    logger.info("デバッグ実行 SQS")

    sqs_main()
