import csv
import logging

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Upload results of db_full spider output to DynamoDB'

    def __init__(self):
        super().__init__()
        self.table = None
        self.logger = logging.getLogger(__name__)

    def add_arguments(self, parser):
        parser.add_argument('csv_path', help='The absolute path to the CSV resource containing exported scrapy items')

    def handle(self, *args, **options):
        dynamodb = boto3.resource('dynamodb', region_name=settings.DYNAMODB_PIPELINE_REGION_NAME,
                                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        self.table = dynamodb.Table(settings.DYNAMODB_PIPELINE_TABLE_NAME)

        with open(options['csv_path']) as f:
            reader = csv.DictReader(f)
            for item in reader:
                self.upload_item(item)

    def upload_item(self, item):
        fingerprint = item['fingerprint']
        url = item['url']

        try:
            self.table.put_item(
                Item={
                    'fingerprint': fingerprint,
                    'url': url,
                    'html': item['html'],
                    'crawled_at': item['crawled_at'],
                },
                ConditionExpression=Attr('fingerprint').ne(fingerprint),
            )
        except ClientError as e:
            error_message = e.response['Error']['Message']
            error_code = e.response['Error']['Code']
            message = f'PutItem failed <url: {url}, fingerprint: {fingerprint}> ({error_code}) {error_message}'

            if error_code == 'ConditionalCheckFailedException':
                self.logger.debug(message)
            else:
                self.logger.error(message)
        else:
            self.logger.debug(f'PutItem succeeded <url: {url}, fingerprint: {fingerprint}>')
