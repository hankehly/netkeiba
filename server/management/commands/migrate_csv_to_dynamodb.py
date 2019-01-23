import csv
import logging

from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


def upload_item(item):
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
        with open(options['csv_path']) as f:
            reader = csv.DictReader(f)

            for item in reader:
                upload_item(item)
