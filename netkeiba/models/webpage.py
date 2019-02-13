import re

from django.db import models
from scrapy import Request
from scrapy.utils.request import request_fingerprint

from netkeiba.models.base import BaseModel
from netkeiba.parsers import Parser, RaceParser, NoopParser


class WebPageManager(models.Manager):
    url_regex = None
    parser_class = NoopParser

    def get_queryset(self):
        qs = super().get_queryset()
        if self.url_regex:
            qs = qs.filter(url__regex=self.url_regex)
        return qs

    def get_by_url(self, url):
        fingerprint = request_fingerprint(Request(url))
        return super().get_queryset().get(fingerprint=fingerprint)


class RaceWebPageManager(WebPageManager):
    """
    Ex. https://db.netkeiba.com/race/201807040211/
    """
    url_regex = '/race/[0-9]+/'
    parser_class = RaceParser


class WebPage(BaseModel):
    url = models.URLField()
    html = models.TextField()
    fingerprint = models.CharField(max_length=255, unique=True)
    crawled_at = models.DateTimeField()

    objects = WebPageManager()
    db_races = RaceWebPageManager()

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
