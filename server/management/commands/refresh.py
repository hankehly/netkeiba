import logging
from datetime import datetime, timedelta

import pytz
from django.core.management import BaseCommand

from netkeiba.settings import TIME_ZONE
from server.models import WebPage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Re-parse and re-persist all HTML for the given page-type'

    def add_arguments(self, parser):
        parser.add_argument('page-type', choices=['race', 'horse'], help='The type of webpage to refresh')

    def handle(self, *args, **options):
        start_time = datetime.now(pytz.timezone(TIME_ZONE))
        logger.info(f'Started import command at {start_time}')

        page_type = options['page-type']
        page_type_regex_map = {'race': 'race/[0-9]+', 'horse': 'horse/[0-9]+'}
        page_type_regex = page_type_regex_map[page_type]
        queryset = WebPage.objects.filter(url__iregex=page_type_regex)
        page_count = queryset.count()

        logger.info(f'About to process {page_count} {page_type} pages')

        i = 1
        for page in queryset.iterator():
            pc_complete = round((i / page_count) * 100)
            current_time = datetime.now(pytz.timezone(TIME_ZONE))
            sec_elapsed = (current_time - start_time).seconds
            sec_remaining = (sec_elapsed / (i / page_count))
            time_remaining = str(timedelta(seconds=round(sec_remaining)))
            logger.info(f'[{i}/{page_count}][{pc_complete}%] {page.url} (estimated time remaining: {time_remaining})')
            parser = page.get_parser()
            parser.parse()
            parser.persist()
            i += 1

        end_time = datetime.now(pytz.timezone(TIME_ZONE))
        duration = str(timedelta(seconds=round((end_time - start_time).seconds)))
        logger.info(f'Finished refresh command at {end_time} ({duration})')
