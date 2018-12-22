import logging

from django.core.management import BaseCommand

from server.models import WebPage

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for page in WebPage.objects.iterator():
            logger.debug(f'Importing {page.url}')
            parser = page.get_parser()
            parser.parse()
            parser.persist()
