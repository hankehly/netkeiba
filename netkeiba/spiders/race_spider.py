import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from netkeiba.items import Horse, RaceFinisher, Jockey, Trainer


class RaceSpiderSpider(scrapy.Spider):
    name = 'race_spider'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']

    def parse(self, response):
        race_list_links = LinkExtractor(allow='/race/list/[0-9]+', restrict_css='.race_calendar') \
            .extract_links(response)

        for link in race_list_links:
            yield scrapy.Request(link.url, callback=self.parse_race_list)

        prev_month_link = LinkExtractor(restrict_css='.race_calendar .rev').extract_links(response)[-1]
        yield scrapy.Request(prev_month_link.url, callback=self.parse)

    def parse_race_list(self, response):
        race_links = LinkExtractor(allow='/race/[0-9]+', restrict_css='.race_list').extract_links(response)

        for link in race_links:
            yield scrapy.Request(link.url, callback=self.parse_race)

    def parse_race(self, response):
        track_details = response.css('.mainrace_data h1+p span::text').extract_first()
        participants = response.css('.race_table_01 tr:not(:first-child)')
        participant_count = len(participants)

        for i, record in enumerate(participants, start=2):
            loader = ItemLoader(item=RaceFinisher(), response=response,
                                selector=response.selector.css(f'.race_table_01 tr:nth-child({i})'))
            loader.default_output_processor = TakeFirst()

            loader.add_css('weight_carried', 'td:nth-child(6)::text')
            loader.add_css('post_position', 'td:nth-child(2) span::text')
            loader.add_css('order_of_finish', 'td:nth-child(1)::text')
            loader.add_css('finish_time', 'td:nth-child(8)::text')
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

            response.meta['race_finisher'] = loader.load_item()

            yield scrapy.Request(response.meta['race_finisher']['horse_url'], callback=self.parse_horse,
                                 meta=response.meta)

    def parse_horse(self, response):
        loader = ItemLoader(item=Horse(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.add_css('total_races', '.db_prof_table tr:nth-last-child(3) td::text')
        loader.add_css('total_wins', '.db_prof_table tr:nth-last-child(3) td::text')
        loader.add_css('sex', '.horse_title .txt_01::text')
        loader.add_css('age', '.horse_title .txt_01::text')
        loader.add_css('rating', '.horse_title .rate strong::text')

        response.meta['horse'] = loader.load_item()

        yield scrapy.Request(response.meta['race_finisher']['jockey_url'], callback=self.parse_jockey,
                             meta=response.meta)

    def parse_jockey(self, response):
        loader = ItemLoader(item=Jockey(), response=response,
                            selector=response.selector.css('table[summary="年度別成績"] tr:nth-child(3)'))
        loader.default_output_processor = TakeFirst()

        loader.add_css('no_1', 'td:nth-child(3) a::text')
        loader.add_css('no_2', 'td:nth-child(4) a::text')
        loader.add_css('no_3', 'td:nth-child(5) a::text')
        loader.add_css('no_4_below', 'td:nth-child(6) a::text')
        loader.add_css('no_turf_races', 'td:nth-child(13) a::text')
        loader.add_css('no_turf_wins', 'td:nth-child(14) a::text')
        loader.add_css('no_dirt_races', 'td:nth-child(15) a::text')
        loader.add_css('no_dirt_wins', 'td:nth-child(16) a::text')
        loader.add_css('place_1_rate', 'td:nth-child(17)::text')
        loader.add_css('place_1_or_2_rate', 'td:nth-child(18)::text')
        loader.add_css('place_any_rate', 'td:nth-child(19)::text')
        loader.add_css('sum_earnings', 'td:nth-child(20)::text')

        response.meta['jockey'] = loader.load_item()

        yield scrapy.Request(response.meta['race_finisher']['trainer_url'], callback=self.parse_trainer,
                             meta=response.meta)

    def parse_trainer(self, response):
        loader = ItemLoader(item=Trainer(), response=response,
                            selector=response.selector.css('table[summary="年度別成績"] tr:nth-child(3)'))
        loader.default_output_processor = TakeFirst()

        loader.add_css('no_1', 'td:nth-child(3) a::text')
        loader.add_css('no_2', 'td:nth-child(4) a::text')
        loader.add_css('no_3', 'td:nth-child(5) a::text')
        loader.add_css('no_4_below', 'td:nth-child(6) a::text')
        loader.add_css('no_turf_races', 'td:nth-child(13) a::text')
        loader.add_css('no_turf_wins', 'td:nth-child(14) a::text')
        loader.add_css('no_dirt_races', 'td:nth-child(15) a::text')
        loader.add_css('no_dirt_wins', 'td:nth-child(16) a::text')
        loader.add_css('place_1_rate', 'td:nth-child(17)::text')
        loader.add_css('place_1_or_2_rate', 'td:nth-child(18)::text')
        loader.add_css('place_any_rate', 'td:nth-child(19)::text')
        loader.add_css('sum_earnings', 'td:nth-child(20)::text')

        trainer = loader.load_item()

        yield {
            'race_finisher': response.meta['race_finisher'],
            'horse': response.meta['horse'],
            'jockey': response.meta['jockey'],
            'trainer': trainer
        }
