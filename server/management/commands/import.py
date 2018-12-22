from django.core.management import BaseCommand

from server.models import WebPage


class Command(BaseCommand):

    def handle(self, *args, **options):
        for page in WebPage.objects.iterator():
            page.get_parser().parse().persist()
