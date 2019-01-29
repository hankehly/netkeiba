import re

from django.db import models

from server.models.base import BaseModel
from server.parsers import Parser, DBHorseParser, DBRaceParser, NoopParser


class WebPageManager(models.Manager):
    url_regex = ''
    parser_class = NoopParser

    def get_queryset(self):
        return super().get_queryset().filter(url__regex=self.url_regex)


class DBHorseWebPageManager(WebPageManager):
    """
    Ex. https://db.netkeiba.com/horse/2015104189/
    """
    url_regex = '/horse/[0-9]+/'
    parser_class = DBHorseParser


class DBRaceWebPageManager(models.Manager):
    """
    Ex. https://db.netkeiba.com/race/201807040211/
    """
    url_regex = '/race/[0-9]+/'
    parser_class = DBRaceParser


class WebPage(BaseModel):
    url = models.URLField()
    html = models.TextField()
    fingerprint = models.CharField(max_length=255, unique=True)
    crawled_at = models.DateTimeField()

    objects = models.Manager()
    db_horses = DBHorseWebPageManager()
    db_races = DBRaceWebPageManager()

    class Meta:
        db_table = 'webpages'

    @classmethod
    def _custom_managers(cls):
        return cls._meta.managers[1:]

    def get_parser(self) -> Parser:
        match = NoopParser
        for manager in self.__class__._custom_managers():
            if re.search(manager.url_regex, self.url):
                match = manager.parser_class
                break
        return match(self.html)
