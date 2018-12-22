import logging
from datetime import timedelta, datetime

import pytz
from django.core.management import call_command

from netkeiba.settings import TIME_ZONE

logger = logging.getLogger(__name__)


def scrape_latest():
    min_date = get_one_week_ago_date_str()
    call_command('scrape', min_date=min_date)


def import_latest():
    min_date = get_one_week_ago_date_str()
    call_command('import', min_date=min_date)


def get_one_week_ago_date_str():
    return (datetime.now(tz=pytz.timezone(TIME_ZONE)) - timedelta(weeks=1)).strftime('%Y-%m-%d')
