# -*- coding: utf-8 -*-

from logging import getLogger
logger = getLogger(__name__)

# import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

from datetime import datetime
from decimal import *
import math

class DynamoService:

    LAST_TABLE_NAME = 'LastOfuro'
    LAST_KEY = 'LAST'

    HIST_TABLE_NAME = 'OfuroHistories'

    def __init__(self,dynamodb):
        self.dynamodb = dynamodb


    def has_dynamodb(self):
        if self.dynamodb == None:
            raise ValueError("dynamodb not set")


    def setup_tables(self):

        self.has_dynamodb()

        self.__setup_last_table()
        self.__setup_history_table()

        return None


    def __setup_history_table(self):
        try:
            table = self.dynamodb.create_table(
                TableName= self.HIST_TABLE_NAME,
                KeySchema=[
                    {
                        'AttributeName': 'UnixTime',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'InOut',
                        'KeyType': 'RANGE'  # Sort key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'UnixTime',
                        'AttributeType': 'N'
                    },
                    {
                        'AttributeName': 'InOut',
                        'AttributeType': 'S'
                    },

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )

            logger.debug(f"Table {self.HIST_TABLE_NAME} created")
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceInUseException':
                raise e


    def __setup_last_table(self):
        try:
            table = self.dynamodb.create_table(
                TableName= self.LAST_TABLE_NAME,
                KeySchema=[
                    {
                        'AttributeName': 'key',
                        'KeyType': 'HASH'  # Partition key
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'key',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )

            logger.debug(f"Table {self.LAST_TABLE_NAME} created")
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceInUseException':
                raise e


    # 最終履歴を取得する
    def get_last_history(self):

        self.has_dynamodb()

        logger.debug(self.dynamodb)

        table = self.dynamodb.Table(self.LAST_TABLE_NAME)

        response = table.query(
            KeyConditionExpression=Key("key").eq(self.LAST_KEY)
        )

        if response['Count'] == 0:
            return None

        return response['Items'][0]['value']


    # 履歴追加エントリポイント
    def put_history(self, inout, lastIn = None):

        self.has_dynamodb()

        history = self.__create_history(inout, lastIn)

        # history作る
        try:
            table = self.dynamodb.Table(self.HIST_TABLE_NAME)
            response = table.put_item(Item=history)

            self.update_last_history(history)

            logger.debug(f'history created')

        except ClientError as e:
            raise e
        else:
            return response


    def __create_history(self, inout, lastIn):

        now = datetime.now()

        result = {
                'UnixTime': Decimal( math.floor( now.timestamp() ) ),
                'InOut': inout,
                'DateTime': now.strftime('%Y%m%d%H%M%S'),
                'LastIn': lastIn
        }
        return result


    # 最新のみを保持するテーブルの更新エントリポイント
    # delete -> insert
    def update_last_history(self, history):
        self.__delete_last_history()
        self.__insert_last_history(history)


    def __insert_last_history(self, history):
        table = self.dynamodb.Table(self.LAST_TABLE_NAME)
        response = table.put_item(
        Item={
                'key': self.LAST_KEY,
                'value': history
            }
        )
        return response


    def __delete_last_history(self):
        try:
            table = self.dynamodb.Table(self.LAST_TABLE_NAME)

            response = table.delete_item(
                Key={
                    'key': self.LAST_KEY
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                logger.error(e.response['Error']['Message'])
            else:
                raise
        else:
            return response
