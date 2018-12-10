import re
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor

from crawler.items import Race, Horse, JockeyResult, TrainerResult


class DataBaseSpider(scrapy.Spider):
    name = 'db'
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
                    f'Skipping <{race_date}> races (minimum race date <{self.settings.get("MIN_RACE_DATE")}>)')

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
        race_key = re.search('[0-9]+', response.request.url).group()
        yield Race(key=race_key, url=response.request.url, html=response.text)

        for link in LinkExtractor(allow='/horse/[0-9]+', restrict_css='.race_table_01').extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_horse)

        for link in LinkExtractor(allow='/jockey/[0-9]+', restrict_css='.race_table_01').extract_links(response):
            jockey_key = re.search('[0-9]+', link.url).group()
            yield scrapy.Request(response.urljoin(f'/jockey/result/{jockey_key}'), callback=self.parse_jockey_result)

        for link in LinkExtractor(allow='/trainer/[0-9]+', restrict_css='.race_table_01').extract_links(response):
            trainer_key = re.search('[0-9]+', link.url).group()
            yield scrapy.Request(response.urljoin(f'/trainer/result/{trainer_key}'), callback=self.parse_trainer_result)

    def parse_horse(self, response):
        horse_key = re.search('[0-9]+', response.request.url).group()
        return Horse(key=horse_key, url=response.request.url, html=response.text)

    def parse_jockey_result(self, response):
        jockey_key = re.search('[0-9]+', response.request.url).group()
        return JockeyResult(key=jockey_key, url=response.request.url, html=response.text)

    def parse_trainer_result(self, response):
        trainer_key = re.search('[0-9]+', response.request.url).group()
        return TrainerResult(key=trainer_key, url=response.request.url, html=response.text)
