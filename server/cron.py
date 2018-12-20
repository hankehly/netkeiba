import logging
from datetime import date, timedelta

from django.core.management import call_command

from server.models import WebPage

logger = logging.getLogger(__name__)


def scrape():
    one_week_ago = (date.today() - timedelta(weeks=1)).strftime('%Y-%m-%d')
    call_command('scrape', min_date=one_week_ago)


def import_scraped_content():
    for page in WebPage.objects.iterator():
        page.get_parser().parse().persist()


dict_model_schema = {
    'horse_key': {'model': 'server.Horse', 'attribute': 'key'}
}


def dict_to_models(data: dict):
    pass
