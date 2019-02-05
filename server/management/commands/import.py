import logging
import os
from datetime import datetime

import pytz
from django.conf import settings
from django.core.management import BaseCommand, CommandError

from netkeiba.settings import TIME_ZONE
from server.models import WebPage

logger = logging.getLogger(__name__)

BLACKLIST = [f'https://db.netkeiba.com/race/{key}/' for key in {
    '199760113001', '199760113005', '199760113008',

    '200143082201', '200143082202', '200143082203', '200143082204', '200143082205', '200143082206',
    '200143082207', '200143082208', '200143082209', '200143082210', '200143082211', '200143082212',

    '200364063001', '200364063002', '200364063003', '200364063004', '200364063005', '200364063006',
    '200364063007', '200364063008', '200364063009', '200364063010', '200364063011',

    '199864071801', '199864071802', '199864071803', '199864071804', '199864071805', '199864071806',
    '199864071807', '199864071808', '199864071809', '199864071810', '199864071811', '199864071812',

    '199864092801', '199864092802', '199864092803', '199864092804', '199864092805', '199864092806',
    '199864092807', '199864092808', '199864092809', '199864092810', '199864092811',

    '199964090601', '199964090602', '199964090603', '199964090604', '199964090605', '199964090606',
    '199964090607', '199964090608', '199964090609', '199964090610', '199964090611',

    '199964070301', '199964070302', '199964070303', '199964070304', '199964070305', '199964070306',
    '199964070307', '199964070308', '199964070309', '199964070310', '199964070311',

    '200064100201', '200064100202', '200064100203', '200064100204', '200064100205', '200064100206',
    '200064100207', '200064100208', '200064100209', '200064100210', '200064100211',

    '200064072201', '200064072202', '200064072203', '200064072204', '200064072205', '200064072206',
    '200064072207', '200064072208', '200064072209', '200064072210', '200064072211',

    '200164092401', '200164092402', '200164092403', '200164092404', '200164092405', '200164092406',
    '200164092407', '200164092408', '200164092409', '200164092410', '200164092411', '200164092412',

    '200264091601', '200264091602', '200264091603', '200264091604', '200264091605', '200264091606',
    '200264091607', '200264091608', '200264091609', '200264091610', '200264091611', '200264091612',

    '200264070601', '200264070602', '200264070603', '200264070604', '200264070605', '200264070606',
    '200264070607', '200264070608', '200264070609', '200264070610', '200264070611', '200264070612',

    '200364070601', '200364070602', '200364070603', '200364070604', '200364070605', '200364070606',
    '200364070607', '200364070608', '200364070609', '200364070610', '200364070611', '200364070612',

    '200364072001', '200364072002', '200364072003', '200364072004', '200364072005', '200364072006',
    '200364072007', '200364072008', '200364072009', '200364072010', '200364072011', '200364072012',
}]


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

        return queryset.exclude(url__in=BLACKLIST).order_by('-crawled_at')

    def handle(self, *args, **options):
        start_time = datetime.now(pytz.timezone(TIME_ZONE))
        logger.info(f'Started import command at {start_time}')

        queryset = self._get_queryset(options.get('scrapy_job_dirname'))

        i = 1
        exception_pages = []
        queryset_count = queryset.count()
        chunk_size = 100

        for j in range(0, queryset_count, chunk_size):
            for page in queryset[j:j + chunk_size]:
                parser = page.get_parser()
                logger.debug(f'({i}/{queryset_count}) {parser.__class__.__name__} <{page.url}>')

                try:
                    parser.parse()
                    parser.persist()
                except Exception as e:
                    logger.exception(e)
                    exception_pages.append(page.url)
                finally:
                    i += 1

        end_time = datetime.now(pytz.timezone(TIME_ZONE))
        duration = (end_time - start_time).seconds
        exception_count = len(exception_pages)
        logger.info(f'Finished import command at {end_time} ({duration} seconds, {exception_count} exceptions)')
