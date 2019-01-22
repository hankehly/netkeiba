import logging
import os

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

from crawler.items import WebPageItem
from server.models.webpage import WebPage


class DjangoPipeline:
    def process_item(self, item, spider):
        if isinstance(item, WebPageItem):
            WebPage.objects.update_or_create(url=item['url'], defaults={'html': item['html']})
        return item


class DynamoDBPipeline:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        table_name = os.getenv('DYNAMODB_TABLE')
        self.table = dynamodb.Table(table_name)
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        fp = item['fingerprint']
        url = item['url']

        try:
            self.table.put_item(
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
                self.logger.debug(message)
            else:
                self.logger.error(message)
                spider.crawler.stats.inc_value('pipeline/dynamodb/failed', spider=spider)
        else:
            spider.crawler.stats.inc_value('pipeline/dynamodb/succeeded', spider=spider)
            msg = f'PutItem succeeded <url: {url}, fingerprint: {fp}>'
            self.logger.debug(msg)
