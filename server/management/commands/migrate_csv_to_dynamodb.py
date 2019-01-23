import csv
import logging

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from django.core.management import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)


def upload_item(table, item):
    fp = item['fingerprint']
    url = item['url']

    try:
        table.put_item(
            Item={
                'fingerprint': fp,
                'url': url,
                'html': item['html'],
                'crawled_at': item['crawled_at'],
            },
            ConditionExpression=Attr('fingerprint').ne(fp),
        )
    except ClientError as e:
        error_message = e.response['Error']['Message']
        error_code = e.response['Error']['Code']
        message = f'PutItem failed <url: {url}, fingerprint: {fp}> ({error_code}) {error_message}'

        if error_code == 'ConditionalCheckFailedException':
            logger.debug(message)
        else:
            logger.error(message)
    else:
        logger.debug(f'PutItem succeeded <url: {url}, fingerprint: {fp}>')


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('csv_path', help='The absolute path to the CSV resource')

    def handle(self, *args, **options):
        dynamodb = boto3.resource('dynamodb', region_name=settings.DYNAMODB_PIPELINE_REGION_NAME, aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        table = dynamodb.Table(settings.DYNAMODB_PIPELINE_TABLE_NAME)

        with open(options['csv_path']) as f:
            reader = csv.DictReader(f)

            for item in reader:
                upload_item(table, item)
