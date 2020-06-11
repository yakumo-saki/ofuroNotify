import boto3
from boto3.session import Session
from concurrent import futures
from src.sqs import sqs_main

import logging
import logging.config

import json
import yaml

import os
import subprocess


def setup_debug_log():
    logging.config.dictConfig(yaml.safe_load(open("logging.yaml").read()))

    # これはすべてのファイルに書く
    logger = logging.getLogger(__name__)

    logger.info("デバッグ実行 SQS")


# テスト用に直接呼び出ししたとき
if __name__ == "__main__":

    setup_debug_log()

    # これはすべてのファイルに書く
    logger = logging.getLogger(__name__)

    logger.info("デバッグ実行 SQS")
    sqs_main()
