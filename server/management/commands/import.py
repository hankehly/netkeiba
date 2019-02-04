import logging
import os
from datetime import datetime

import pytz
from django.conf import settings
from django.core.management import BaseCommand, CommandError

from netkeiba.settings import TIME_ZONE
from server.parsers.race import RaceParser
from server.models import WebPage, RaceContender

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Extract, clean and persist scraped netkeiba HTML'

    def add_arguments(self, parser):
        parser.add_argument('--scrapy-job-dirname', help='The name of the scrapy crawl jobdir')
        parser.add_argument('-a', '--all', action='store_true', help='Parse all pages')

    def handle(self, *args, **options):
        start_time = datetime.now(pytz.timezone(TIME_ZONE))
        logger.info(f'Started import command at {start_time}')

        if options['all']:
            queryset = WebPage.objects.all()
        else:
            crawls_dir = os.path.join(settings.TMP_DIR, 'crawls')
            requests_seen = os.path.join(crawls_dir, options['scrapy-job-dirname'], 'requests.seen')

            if not os.path.exists(requests_seen):
                raise CommandError('jobdir/requests.seen does not exist')

            fingerprints = open(requests_seen).read().splitlines()
            queryset = WebPage.objects.filter(fingerprint__in=fingerprints).order_by('-updated_at')

        i = 1
        exception_count = 0
        count = queryset.count()
        blacklist = [
            # pages that are buggy and missing content
            'https://db.netkeiba.com/race/200143082201/'
        ]

        for page in queryset.exclude(url__in=blacklist).iterator():
            parser = page.get_parser()

            logger.debug(f'({i}/{count}) {parser.__class__.__name__} <{page.url}>')

            try:
                parser.parse()
                parser.persist()
            except Exception as e:
                logger.exception(e)
                exception_count += 1
            finally:
                i += 1

        end_time = datetime.now(pytz.timezone(TIME_ZONE))
        duration = (end_time - start_time).seconds
        logger.info(f'Finished import command at {end_time} ({duration} seconds, {exception_count} exceptions)')
