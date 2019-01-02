import logging
import os
from datetime import datetime

import pytz
from django.conf import settings
from django.core.management import BaseCommand, CommandError

from netkeiba.settings import TIME_ZONE
from crawler.parsers.race import RaceParser
from server.models import WebPage, RaceContender

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Extract, clean and persist scraped netkeiba HTML'

    def add_arguments(self, parser):
        parser.add_argument('scrapy-job-dirname', help='The name of the scrapy crawl jobdir')

    def handle(self, *args, **options):
        start_time = datetime.now(pytz.timezone(TIME_ZONE))
        logger.info(f'Started import command at {start_time}')

        crawls_dir = os.path.join(settings.TMP_DIR, 'crawls')
        requests_seen = os.path.join(crawls_dir, options['scrapy-job-dirname'], 'requests.seen')

        if not os.path.exists(requests_seen):
            raise CommandError('jobdir/requests.seen does not exist')

        fingerprints = open(requests_seen).read().splitlines()
        queryset = WebPage.objects.filter(fingerprint__in=fingerprints).order_by('-updated_at')

        i = 1
        exception_count = 0
        page_count = queryset.count()

        for page in queryset.iterator():
            parser = page.get_parser()

            logger.debug(f'({i}/{page_count}) parsing {page.url} with {parser.__class__.__name__}')

            try:
                parser.parse()

                if isinstance(parser, RaceParser):
                    pre_save_contender_count = RaceContender.objects.count()
                    parsed_contender_count = len(parser.data.get('contenders'))
                    parser.persist()
                    post_save_contender_count = RaceContender.objects.count()
                    logger.debug(
                        f'parsed {parsed_contender_count} contenders (total: {pre_save_contender_count} -> {post_save_contender_count})')
                else:
                    parser.persist()
            except Exception as e:
                logger.exception(e)
                exception_count += 1
            finally:
                i += 1

        end_time = datetime.now(pytz.timezone(TIME_ZONE))
        duration = (end_time - start_time).seconds
        logger.info(f'Finished import command at {end_time} ({duration} seconds, {exception_count} exceptions)')
