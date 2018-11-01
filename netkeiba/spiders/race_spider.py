import re
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from netkeiba.items import Horse, RaceFinisher, Jockey, Trainer


class RaceSpider(scrapy.Spider):
    name = 'race_spider'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']

    custom_settings = {
        'MIN_RACE_DATE': '2018-01-01'
    }

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
        track_details = response.css('.mainrace_data h1+p span::text').extract_first()
        participants = response.css('.race_table_01 tr:not(:first-child)')
        race_details = response.css('.mainrace_data .smalltxt::text').extract_first()
        participant_count = len(participants)

        for i, record in enumerate(participants, start=2):
            loader = ItemLoader(item=RaceFinisher(), response=response,
                                selector=response.selector.css(f'.race_table_01 tr:nth-child({i})'))
            loader.default_output_processor = TakeFirst()

            loader.add_css('weight_carried', 'td:nth-child(6)::text')
            loader.add_css('horse_sex', 'td:nth-child(5)::text')
            loader.add_css('horse_age', 'td:nth-child(5)::text')
            loader.add_css('post_position', 'td:nth-child(2) span::text')
            loader.add_css('order_of_finish', 'td:nth-child(1)::text')
            loader.add_css('finish_time_seconds', 'td:nth-child(8)::text')
            loader.add_value('distance_meters', track_details)
            loader.add_value('weather', track_details)
            loader.add_value('direction', track_details)
            loader.add_value('track_condition', track_details)
            loader.add_value('track_type', track_details)
            loader.add_value('race_url', response.request.url)
            loader.add_css('horse_url', 'td:nth-child(4) a::attr(href)')
            loader.add_css('jockey_url', 'td:nth-child(7) a::attr(href)')
            loader.add_value('trainer_url', record.css('*').extract_first())
            loader.add_value('participant_count', participant_count)
            loader.add_value('race_date', race_details)
            loader.add_value('race_location', race_details)

            # for some reason, nth-child fails to access the following columns by index
            loader.add_value('first_place_odds', record.css('td')[12].css('::text').extract_first())
            loader.add_value('popularity', record.css('td')[13].css('::text').extract_first())
            loader.add_value('horse_weight', record.css('td')[14].css('::text').extract_first())

            response.meta['race_finisher'] = loader.load_item()

            yield scrapy.Request(response.meta['race_finisher']['horse_url'], callback=self.parse_horse,
                                 meta=response.meta, dont_filter=True)

    def parse_horse(self, response):
        loader = ItemLoader(item=Horse(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.add_css('total_races', '.db_prof_table tr:nth-last-child(3) td::text')
        loader.add_css('total_wins', '.db_prof_table tr:nth-last-child(3) td::text')
        loader.add_css('rating', '.horse_title .rate strong::text')

        response.meta['horse'] = loader.load_item()

        return scrapy.Request(response.meta['race_finisher']['jockey_url'], callback=self.parse_jockey,
                             meta=response.meta, dont_filter=True)

    def parse_jockey(self, response):
        loader = ItemLoader(item=Jockey(), response=response,
                            selector=response.selector.css('table[summary="年度別成績"] tr:nth-child(3)'))
        loader.default_output_processor = TakeFirst()

        loader.add_css('num_1_place', 'td:nth-child(3) a::text')
        loader.add_css('num_2_place', 'td:nth-child(4) a::text')
        loader.add_css('num_3_place', 'td:nth-child(5) a::text')
        loader.add_css('num_4_below', 'td:nth-child(6) a::text')
        loader.add_css('num_turf_races', 'td:nth-child(13) a::text')
        loader.add_css('num_turf_wins', 'td:nth-child(14) a::text')
        loader.add_css('num_dirt_races', 'td:nth-child(15) a::text')
        loader.add_css('num_dirt_wins', 'td:nth-child(16) a::text')
        loader.add_css('place_1_rate', 'td:nth-child(17)::text')
        loader.add_css('place_1_or_2_rate', 'td:nth-child(18)::text')
        loader.add_css('place_any_rate', 'td:nth-child(19)::text')
        loader.add_css('sum_earnings', 'td:nth-child(20)::text')

        response.meta['jockey'] = loader.load_item()

        return scrapy.Request(response.meta['race_finisher']['trainer_url'], callback=self.parse_trainer,
                             meta=response.meta, dont_filter=True)

    def parse_trainer(self, response):
        loader = ItemLoader(item=Trainer(), response=response,
                            selector=response.selector.css('table[summary="年度別成績"] tr:nth-child(3)'))
        loader.default_output_processor = TakeFirst()

        loader.add_css('num_1_place', 'td:nth-child(3) a::text')
        loader.add_css('num_2_place', 'td:nth-child(4) a::text')
        loader.add_css('num_3_place', 'td:nth-child(5) a::text')
        loader.add_css('num_4_below', 'td:nth-child(6) a::text')
        loader.add_css('num_turf_races', 'td:nth-child(13) a::text')
        loader.add_css('num_turf_wins', 'td:nth-child(14) a::text')
        loader.add_css('num_dirt_races', 'td:nth-child(15) a::text')
        loader.add_css('num_dirt_wins', 'td:nth-child(16) a::text')
        loader.add_css('place_1_rate', 'td:nth-child(17)::text')
        loader.add_css('place_1_or_2_rate', 'td:nth-child(18)::text')
        loader.add_css('place_any_rate', 'td:nth-child(19)::text')
        loader.add_css('sum_earnings', 'td:nth-child(20)::text')

        trainer = loader.load_item()

        return {
            'race_finisher': response.meta['race_finisher'],
            'horse': response.meta['horse'],
            'jockey': response.meta['jockey'],
            'trainer': trainer
        }
