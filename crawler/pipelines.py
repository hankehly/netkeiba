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

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, table_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.table_name = table_name
        self.table = None
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        aws_access_key_id = crawler.settings['AWS_ACCESS_KEY_ID']
        aws_secret_access_key = crawler.settings['AWS_SECRET_ACCESS_KEY']
        region_name = crawler.settings['DYNAMODB_PIPELINE_REGION_NAME']
        table_name = crawler.settings['DYNAMODB_PIPELINE_TABLE_NAME']
        return cls(region_name=region_name, table_name=table_name, aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key)

    def open_spider(self, spider):
        dynamodb = boto3.resource('dynamodb', region_name=self.region_name, aws_access_key_id=self.aws_access_key_id,
                                  aws_secret_access_key=self.aws_secret_access_key)
        self.table = dynamodb.Table(self.table_name)

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
