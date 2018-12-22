import re

from django.db import models

from crawler.parsers.parser import Parser
from crawler.parsers.horse import HorseParser
from crawler.parsers.jockey_result import JockeyResultParser
from crawler.parsers.race import RaceParser
from crawler.parsers.trainer_result import TrainerResultParser
from crawler.parsers.noop import NoopParser
from server.models.base import BaseModel


class WebPage(BaseModel):
    url = models.URLField(unique=True)
    html = models.TextField()

    class Meta:
        db_table = 'webpages'

    def get_parser(self) -> Parser:
        parser_lookup_table = [
            {'regex': '/horse/[0-9]+/', 'class': HorseParser},
            # {'regex': '/jockey/result/[0-9]+/', 'class': JockeyResultParser},
            # {'regex': '/race/[0-9]+/', 'class': RaceParser},
            # {'regex': '/trainer/result/[0-9]+/', 'class': TrainerResultParser},
        ]

        parser_class = NoopParser
        for row in parser_lookup_table:
            if re.search(row['regex'], self.url):
                parser_class = row['class']
                break

        return parser_class(self.html)
