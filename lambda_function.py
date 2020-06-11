import boto3
from boto3.session import Session
from concurrent import futures
from src.main import main_process

import logging
import logging.config
import yaml

import json

import os
import subprocess


# lambda から呼び出されたときのエントリポイント
def lambda_handler(event, context):

    logging.config.dictConfig(yaml.safe_load(open("logging.yaml").read()))

    logger = logging.getLogger(__name__)

    dynamodb = boto3.resource('dynamodb')

    main_process(dynamodb, event, context)

    return {
        'statusCode': 200,
        'body': json.dumps('Done!')
    }

