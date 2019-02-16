import logging
import os
from concurrent.futures import as_completed, ThreadPoolExecutor

from datetime import datetime

import pytz
from django.core.management import BaseCommand, CommandError

from netkeiba import settings
from netkeiba.models import WebPage

logger = logging.getLogger(__name__)


def import_page(queryset, i):
    page = queryset[i]
    parser = page.get_parser()
    try:
        parser.parse()
        parser.persist()
    except Exception as e:
        raise e
    return page.url


class Command(BaseCommand):
    help = 'Extract, clean and persist scraped netkeiba HTML'

    def add_arguments(self, parser):
        parser.add_argument('--scrapy-job-dirname', help='The name of the scrapy crawl jobdir')
        parser.add_argument('--offset', type=int, help='Start parsing web pages from {offset}', default=0)

    def _get_queryset(self, scrapy_job_dirname=None):
        if scrapy_job_dirname:
            requests_seen = os.path.join(settings.TMP_DIR, 'crawls', scrapy_job_dirname, 'requests.seen')

            if not os.path.exists(requests_seen):
                raise CommandError('jobdir/requests.seen does not exist')

            fingerprints = open(requests_seen).read().splitlines()
            queryset = WebPage.objects.filter(fingerprint__in=fingerprints)
        else:
            queryset = WebPage.objects.all()

        return queryset

    def handle(self, *args, **options):
        started_at = datetime.now(pytz.timezone(settings.TIME_ZONE))
        logger.info(f'START <{started_at}>')

        queryset = self._get_queryset(options.get('scrapy_job_dirname'))
        count = queryset.count()

        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_ix = {executor.submit(import_page, queryset, i): i for i in range(options['offset'], count)}
            for future in as_completed(future_to_ix):
                row = future_to_ix[future] + 1
                try:
                    url = future.result()
                except Exception as e:
                    logger.exception(e)
                else:
                    logger.info(f'({row}/{count}) <{url}>')

        stopped_at = datetime.now(pytz.timezone(settings.TIME_ZONE))
        duration = (stopped_at - started_at).seconds
        logger.info(f'STOP <{stopped_at}, duration: {duration} seconds>')
