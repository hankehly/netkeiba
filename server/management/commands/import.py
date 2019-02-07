import logging
import os
import uuid

import pandas as pd
from datetime import datetime

import pytz
from django.conf import settings
from django.core.management import BaseCommand, CommandError

from netkeiba.settings import TIME_ZONE
from server.models import WebPage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Extract, clean and persist scraped netkeiba HTML'

    def add_arguments(self, parser):
        parser.add_argument('--scrapy-job-dirname', help='The name of the scrapy crawl jobdir')

    def _get_queryset(self, scrapy_job_dirname=None):
        if scrapy_job_dirname:
            crawls_dir = os.path.join(settings.TMP_DIR, 'crawls')
            requests_seen = os.path.join(crawls_dir, scrapy_job_dirname, 'requests.seen')

            if not os.path.exists(requests_seen):
                raise CommandError('jobdir/requests.seen does not exist')

            fingerprints = open(requests_seen).read().splitlines()
            queryset = WebPage.objects.filter(fingerprint__in=fingerprints)
        else:
            queryset = WebPage.objects.all()

        return queryset

    def handle(self, *args, **options):
        start_time = datetime.now(pytz.timezone(TIME_ZONE))
        logger.info(f'START')
        queryset = self._get_queryset(options.get('scrapy_job_dirname'))

        i = 1
        exceptions = []
        queryset_count = queryset.count()
        chunk_size = 100

        # rolling our own iterator logic
        # due to bad `.iterator` performance
        for j in range(0, queryset_count, chunk_size):
            for page in queryset[j:j + chunk_size]:
                parser = page.get_parser()
                logger.info(f'({i}/{queryset_count}) {parser.__class__.__name__} <{page.url}>')
                try:
                    parser.parse()
                    parser.persist()
                except Exception as e:
                    logger.exception(e)
                    exceptions.append([page.url, str(e)])
                finally:
                    i += 1

        stop_time = datetime.now(pytz.timezone(TIME_ZONE))
        duration = (stop_time - start_time).seconds
        exception_count = len(exceptions)
        logger.info(f'STOP <{duration} seconds, {exception_count} exceptions>')
        uid = str(uuid.uuid4())
        exceptions_csv_path = os.path.join(settings.TMP_DIR, f'exceptions_{uid}.csv')
        pd.DataFrame(exceptions, columns=['url', 'message']).to_csv(exceptions_csv_path)
