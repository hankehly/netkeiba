import re
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor

from netkeiba.items import RaceRequest, JockeyRequest, TrainerRequest, HorseRequest


class DataBaseSpider(scrapy.Spider):
    name = 'database'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']

    def parse(self, response):
        min_race_date = datetime.strptime(self.settings.get('MIN_RACE_DATE'), '%Y-%m-%d').date()

        race_list_links = LinkExtractor(allow='/race/list/[0-9]+', restrict_css='.race_calendar') \
            .extract_links(response)

        for link in race_list_links:
            race_date = datetime.strptime(re.search('/race/list/([0-9]+)', link.url).group(1), '%Y%m%d').date()
            if race_date >= min_race_date:
                yield scrapy.Request(link.url, callback=self.parse_race_list)
            else:
                self.logger.info(
                    f'Skipped <{race_date}> races (minimum race date <{self.settings.get("MIN_RACE_DATE")}>)')

        rev_links = LinkExtractor(restrict_css='.race_calendar .rev').extract_links(response)

        if len(rev_links) > 1:
            prev_page_link = rev_links[-1]
            prev_page_date_str = re.search('date=([0-9]+)$', prev_page_link.url).group(1)
            prev_page_date = datetime.strptime(prev_page_date_str, '%Y%m%d').date()
            if prev_page_date >= min_race_date:
                yield scrapy.Request(prev_page_link.url, callback=self.parse)
            else:
                self.logger.info(f'Reached minimum race date ({min_race_date})')

    def parse_race_list(self, response):
        race_links = LinkExtractor(allow='/race/[0-9]+', restrict_css='.race_list').extract_links(response)

        for link in race_links:
            yield scrapy.Request(link.url, callback=self.parse_race)

    def parse_race(self, response):
        race_id = re.search('[0-9]+', response.request.url).group()
        yield RaceRequest(item_type='race', id=race_id, url=response.request.url, response_body=response.text)

        for link in LinkExtractor(allow='/horse/[0-9]+', restrict_css='.race_table_01').extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_horse)

        for link in LinkExtractor(allow='/jockey/[0-9]+', restrict_css='.race_table_01').extract_links(response):
            jockey_id = re.search('[0-9]+', link.url).group()
            yield scrapy.Request(response.urljoin(f'/jockey/result/{jockey_id}'), callback=self.parse_jockey)

        for link in LinkExtractor(allow='/trainer/[0-9]+', restrict_css='.race_table_01').extract_links(response):
            trainer_id = re.search('[0-9]+', link.url).group()
            yield scrapy.Request(response.urljoin(f'/trainer/result/{trainer_id}'), callback=self.parse_trainer)

    def parse_horse(self, response):
        horse_id = re.search('[0-9]+', response.request.url).group()
        return HorseRequest(item_type='horse', id=horse_id, url=response.request.url, response_body=response.text)

    def parse_jockey(self, response):
        jockey_id = re.search('[0-9]+', response.request.url).group()
        return JockeyRequest(item_type='jockey', id=jockey_id, url=response.request.url, response_body=response.text)

    def parse_trainer(self, response):
        trainer_id = re.search('[0-9]+', response.request.url).group()
        return TrainerRequest(item_type='trainer', id=trainer_id, url=response.request.url, response_body=response.text)
