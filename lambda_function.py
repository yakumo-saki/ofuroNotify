import boto3
from boto3.session import Session
from concurrent import futures
from src.main import main_process

import json

import os
import subprocess

# lambda から呼び出されたときのエントリポイント
def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')

    main_process(dynamodb, event, context)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

