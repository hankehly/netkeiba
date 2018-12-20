import re

from django.db import models

from crawler.parsers.parser import Parser
from crawler.parsers.horse import HorseParser
from crawler.parsers.jockey_result import JockeyResultParser
from crawler.parsers.race import RaceParser
from crawler.parsers.trainer_result import TrainerResultParser
from server.models.base import BaseModel


class WebPage(BaseModel):
    url = models.URLField(unique=True)
    html = models.TextField()

    class Meta:
        db_table = 'webpages'

    def get_parser(self) -> Parser:
        parser_class = None

        if re.search('/horse/[0-9]+/', self.url):
            parser_class = HorseParser
        elif re.search('/jockey/result/[0-9]+/', self.url):
            parser_class = JockeyResultParser
        elif re.search('/race/[0-9]+/', self.url):
            parser_class = RaceParser
        elif re.search('/trainer/result/[0-9]+/', self.url):
            parser_class = TrainerResultParser

        # TODO: Add parsers for
        # - https://db.netkeiba.com/jockey/01171/
        # - https://db.netkeiba.com/jockey/profile/01171/
        # - https://db.netkeiba.com/trainer/01057/
        # - https://db.netkeiba.com/trainer/profile/01057/

        if not parser_class:
            raise ValueError(f'WebPage({self.pk}) has no parser')

        return parser_class(self.html)
