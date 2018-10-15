import re

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
            horse_sex, horse_age = parse_horse_sex_age(record)
            post_position = record.css('td:nth-child(2) span::text').extract_first()
            weight_carried = record.css('td:nth-child(6)::text').extract_first()
            horse_profile_href = record.css('td:nth-child(4) a::attr(href)').extract_first()

            jockey_results_href = record.css('td:nth-child(7) a::attr(href)').extract_first()
            jockey_href_comps = _filter_empty(jockey_results_href.split('/'))
            jockey_href_comps.insert(1, 'result')
            jockey_results_href = '/' + '/'.join(jockey_href_comps)

            race = Race(
                detail_text=response.css('.mainrace_data h1+p span::text').extract_first(),
                weight_carried=weight_carried,
                horse_sex=horse_sex,
                horse_age=horse_age,
                post_position=post_position,
                order_of_finish=parse_order_of_finish(record),
                race_url=response.request.url,
                horse_profile=response.urljoin(horse_profile_href),
                jockey_record=response.urljoin(jockey_results_href)
            )

            yield scrapy.Request(race['horse_profile'], callback=self.parse_horse_profile, meta={'race': race})

    def parse_horse_profile(self, response):
        race = response.meta['race']
        prof_table_rows = response.css('.db_prof_table tr')
        win_record_ix = len(prof_table_rows) - 2
        win_record = response.css(f'.db_prof_table tr:nth-child({win_record_ix}) td::text').extract_first()
        race['horse_num_races'], race['horse_previous_wins'] = re.split('[戦勝]', win_record)[:2]
        yield scrapy.Request(race['jockey_record'], callback=self.parse_jockey_record, meta={'race': race})

    def parse_jockey_record(self, response):
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
        return race


def parse_horse_sex_age(record):
    gender_map = {
        '牡': 'male',
        '牝': 'female',
        'セ': 'castrated'
    }
    text_attr = record.css('td:nth-child(5)::text').extract_first()
    return gender_map.get(text_attr[0]), text_attr[1]


def parse_order_of_finish(record):
    return record.css('td:nth-child(1)::text').extract_first()


def parse_finish_time(record):
    finish_time_str = record.css('td:nth-child(8)::text').extract_first()

    if finish_time_str is None:
        return None

    minutes, seconds = map(float, finish_time_str.split(':'))
    return minutes * 60 + seconds
