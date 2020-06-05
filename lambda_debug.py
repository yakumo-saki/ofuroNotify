import boto3
from boto3.session import Session
from concurrent import futures
from src.main import main_process

import json

import os
import subprocess


# テスト用に直接呼び出ししたとき
if __name__ == "__main__":

    print("デバッグ実行")
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', use_ssl=False, endpoint_url="http://localhost:8000",
					aws_access_key_id='local', aws_secret_access_key='local')
    main_process(dynamodb, None, None)
