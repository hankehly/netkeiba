import logging
from datetime import timedelta, datetime

import pytz
from django.core.management import call_command

from netkeiba.settings import TIME_ZONE

logger = logging.getLogger(__name__)


def process_latest():
    one_week_ago = (datetime.now(tz=pytz.timezone(TIME_ZONE)) - timedelta(weeks=1)).strftime('%Y-%m-%d')
    call_command('scrape', min_date=one_week_ago)
    call_command('import', min_date=one_week_ago)
    call_command('backup')
