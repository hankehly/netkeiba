import os
from datetime import datetime

import pytz
from django.conf import settings
from django.core.management import BaseCommand
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from twisted.internet import reactor


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        crawls_dir = os.path.join(settings.TMP_DIR, 'crawls')
        if not os.path.isdir(crawls_dir):
            os.mkdir(crawls_dir)

        piddir = os.path.join(settings.TMP_DIR, 'pids')
        if not os.path.isdir(piddir):
            os.mkdir(piddir)

        job_timestamp = datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%dT%H%M%S')
        jobpath = os.path.join(crawls_dir, job_timestamp)
        os.mkdir(jobpath)

        pidfile = os.path.join(piddir, f'{job_timestamp}.pid')
        with open(pidfile, 'w') as f:
            f.write(str(os.getpid()) + os.linesep)

        s3_pipeline_url_components = [
            's3://', settings.AWS_BUCKET, '/crawls/{name}/', job_timestamp, '/items.{chunk:07d}.jl.gz']

        custom_settings = {
            'S3PIPELINE_MAX_CHUNK_SIZE': 100,
            'JOBDIR': jobpath,
            'ITEM_PIPELINES': {'s3pipeline.S3Pipeline': 100},
            'S3PIPELINE_URL': ''.join(s3_pipeline_url_components),
        }

        scrapy_settings = Settings()
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'crawler.settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        scrapy_settings.setmodule(settings_module_path, priority='project')

        runner = CrawlerRunner({**scrapy_settings, **custom_settings})
        d = runner.crawl('db_full')
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
