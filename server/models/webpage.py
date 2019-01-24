import re

from django.db import models

from crawler.parsers.parser import Parser
from crawler.parsers.horse import HorseParser
from crawler.parsers.jockey_result import JockeyResultParser
from crawler.parsers.db_race import DBRaceParser
from crawler.parsers.trainer_result import TrainerResultParser
from crawler.parsers.noop import NoopParser
from server.models.base import BaseModel


class WebPage(BaseModel):
    url = models.URLField(unique=True)
    html = models.TextField()
    fingerprint = models.CharField(max_length=255)
    crawled_at = models.DateTimeField()

    class Meta:
        db_table = 'webpages'

    def get_parser(self) -> Parser:
        parser_lookup_table = [
            {'regex': '/horse/[0-9]+/', 'class': HorseParser},
            {'regex': '/jockey/result/[0-9]+/', 'class': JockeyResultParser},
            {'regex': '/race/[0-9]+/', 'class': DBRaceParser},
            {'regex': '/trainer/result/[0-9]+/', 'class': TrainerResultParser},
        ]

        parser_class = NoopParser
        for row in parser_lookup_table:
            if re.search(row['regex'], self.url):
                parser_class = row['class']
                break

        return parser_class(self.html)


# class DBHorseWebPageManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(url__regex='')
#
#
# class DBHorseWebPage(WebPage):
#     objects = DBHorseWebPageManager()
#
#     class Meta:
#         proxy = True
#
#     def parse(self):
#         key = self._parse_key()
#         total_races = self._parse_total_races()
#         total_wins = self._parse_total_wins()
#         birthday = self._parse_birthday()
#         sex = self._parse_sex()
#         user_rating = self._parse_user_rating()
#         name = self._parse_name()
#
#         self.data = {
#             'key': key,
#             'total_races': total_races,
#             'total_wins': total_wins,
#             'birthday': birthday,
#             'sex': sex,
#             'user_rating': user_rating,
#             'name': name,
#         }
#
#     def persist(self):
#         pass
