import re
from urllib.parse import urlparse, urlunparse

import scrapy
from scrapy.linkextractors import LinkExtractor

from netkeiba.items import Race
from netkeiba.pipelines import _filter_empty


class RaceSpiderSpider(scrapy.Spider):
    name = 'race_spider'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']

    def parse(self, response):
        race_list_links = LinkExtractor(allow=r'\/race\/list\/[0-9]+', restrict_css='.race_calendar') \
            .extract_links(response)

        for link in race_list_links:
            yield scrapy.Request(link.url, callback=self.parse_race_list)

        prev_month_link = LinkExtractor(restrict_css='.race_calendar .rev').extract_links(response)[-1]
        yield scrapy.Request(prev_month_link.url, callback=self.parse)

    def parse_race_list(self, response):
        race_links = LinkExtractor(allow=r'\/race\/[0-9]+', restrict_css='.race_list').extract_links(response)

        for link in race_links:
            yield scrapy.Request(link.url, callback=self.parse_race)

    def parse_race(self, response):
        for record in response.css('table[summary="レース結果"] tr:not(:first-child)'):
            race = Race()

            race['weight_carried'] = record.css('td:nth-child(6)::text').extract_first()
            race['horse_sex_age'] = record.css('td:nth-child(5)::text').extract_first()
            race['post_position'] = record.css('td:nth-child(2) span::text').extract_first()
            race['order_of_finish'] = record.css('td:nth-child(1)::text').extract_first()
            race['finish_time'] = record.css('td:nth-child(8)::text').extract_first()
            race['race_url'] = response.request.url
            race['horse'] = response.urljoin(record.css('td:nth-child(4) a::attr(href)').extract_first())
            race['race_header_text'] = response.css('.mainrace_data h1+p span::text').extract_first()

            jockey_href = record.css('td:nth-child(7) a::attr(href)').extract_first()
            jockey_href_split = _filter_empty(jockey_href.split('/'))
            jockey_href_split.insert(1, 'result')
            jockey_href = '/' + '/'.join(jockey_href_split)
            race['jockey'] = response.urljoin(jockey_href)

            trainer_url_str = LinkExtractor(allow=r'\/trainer\/[0-9]+', restrict_css='.race_table_01 tr:nth-child(2)') \
                .extract_links(response)[0].url
            trainer_url = urlparse(trainer_url_str)
            trainer_id = re.match(r'/trainer/([0-9]+)/', trainer_url.path).group(1)
            trainer_result_url = trainer_url._replace(path=f'/trainer/result/{trainer_id}')
            race['trainer'] = urlunparse(trainer_result_url)

            yield scrapy.Request(race['horse'], callback=self.parse_horse, meta={'race': race})

    def parse_horse(self, response):
        race = response.meta['race']

        win_record = response.css('.db_prof_table tr:nth-last-child(3) td::text').extract_first()
        race['horse_no_races'], race['horse_no_wins'] = re.split('[戦勝]', win_record)[:2]

        yield scrapy.Request(race['jockey'], callback=self.parse_jockey, meta={'race': race})

    def parse_jockey(self, response):
        race = response.meta['race']

        totals = response.css('table[summary="年度別成績"] tr:nth-child(3)')
        race['jockey_no_1'] = totals.css('td:nth-child(3) a::text').extract_first()
        race['jockey_no_2'] = totals.css('td:nth-child(4) a::text').extract_first()
        race['jockey_no_3'] = totals.css('td:nth-child(5) a::text').extract_first()
        race['jockey_no_4_below'] = totals.css('td:nth-child(6) a::text').extract_first()
        race['jockey_no_turf_races'] = totals.css('td:nth-child(13) a::text').extract_first()
        race['jockey_no_turf_wins'] = totals.css('td:nth-child(14) a::text').extract_first()
        race['jockey_no_dirt_races'] = totals.css('td:nth-child(15) a::text').extract_first()
        race['jockey_no_dirt_wins'] = totals.css('td:nth-child(16) a::text').extract_first()
        race['jockey_1_rate'] = totals.css('td:nth-child(17)::text').extract_first()
        race['jockey_1_2_rate'] = totals.css('td:nth-child(18)::text').extract_first()
        race['jockey_place_rate'] = totals.css('td:nth-child(19)::text').extract_first()
        race['jockey_sum_earnings'] = totals.css('td:nth-child(20)::text').extract_first()

        yield scrapy.Request(race['trainer'], callback=self.parse_trainer, meta={'race': race})

    def parse_trainer(self, response):
        race = response.meta['race']
        yield race
