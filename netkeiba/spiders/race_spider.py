import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from netkeiba.items import Horse, RaceFinish


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
        race_details = response.css('.mainrace_data h1+p span::text').extract_first()

        for i, record in enumerate(response.css('.race_table_01 tr:not(:first-child)'), start=2):
            loader = ItemLoader(item=RaceFinish(), response=response,
                                selector=response.selector.css(f'.race_table_01 tr:nth-child({i})'))
            loader.default_output_processor = TakeFirst()

            loader.add_css('weight_carried', 'td:nth-child(6)::text')
            loader.add_css('post_position', 'td:nth-child(2) span::text')
            loader.add_css('order_of_finish', 'td:nth-child(1)::text')
            loader.add_css('finish_time', 'td:nth-child(8)::text')
            loader.add_value('distance_meters', race_details)
            loader.add_value('weather', race_details)
            loader.add_value('direction', race_details)
            loader.add_value('race_url', response.request.url)
            loader.add_css('horse', 'td:nth-child(4) a::attr(href)')
            loader.add_css('jockey', 'td:nth-child(7) a::attr(href)')
            loader.add_value('trainer', record.css('*').extract_first())

            response.meta['race_finish_item'] = loader.load_item()

            yield scrapy.Request(response.meta['race_finish_item']['horse'], callback=self.parse_horse,
                                 meta=response.meta)

    def parse_horse(self, response):
        loader = ItemLoader(item=Horse(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.add_css('total_races', '.db_prof_table tr:nth-last-child(3) td::text')
        loader.add_css('total_wins', '.db_prof_table tr:nth-last-child(3) td::text')
        loader.add_css('sex', '.horse_title .txt_01::text')
        loader.add_css('age', '.horse_title .txt_01::text')
        loader.add_css('rating', '.horse_title .rate strong::text')

        response.meta['horse_item'] = loader.load_item()

        return response.meta

        # yield scrapy.Request(response.meta['race_finish_item']['jockey'], callback=self.parse_jockey,
        #                      meta=response.meta)

    def parse_jockey(self, response):
        # race = response.meta['race']
        #
        # totals = response.css('table[summary="年度別成績"] tr:nth-child(3)')
        # race['jockey_no_1'] = totals.css('td:nth-child(3) a::text').extract_first()
        # race['jockey_no_2'] = totals.css('td:nth-child(4) a::text').extract_first()
        # race['jockey_no_3'] = totals.css('td:nth-child(5) a::text').extract_first()
        # race['jockey_no_4_below'] = totals.css('td:nth-child(6) a::text').extract_first()
        # race['jockey_no_turf_races'] = totals.css('td:nth-child(13) a::text').extract_first()
        # race['jockey_no_turf_wins'] = totals.css('td:nth-child(14) a::text').extract_first()
        # race['jockey_no_dirt_races'] = totals.css('td:nth-child(15) a::text').extract_first()
        # race['jockey_no_dirt_wins'] = totals.css('td:nth-child(16) a::text').extract_first()
        # race['jockey_1_rate'] = totals.css('td:nth-child(17)::text').extract_first()
        # race['jockey_1_2_rate'] = totals.css('td:nth-child(18)::text').extract_first()
        # race['jockey_place_rate'] = totals.css('td:nth-child(19)::text').extract_first()
        # race['jockey_sum_earnings'] = totals.css('td:nth-child(20)::text').extract_first()

        # yield scrapy.Request(race['trainer'], callback=self.parse_trainer, meta={'race': race})
        pass

    def parse_trainer(self, response):
        race = response.meta['race']

        totals = response.css('table[summary="年度別成績"] tr:nth-child(3)')
        race['trainer_no_1'] = totals.css('td:nth-child(3) a::text').extract_first()
        race['trainer_no_2'] = totals.css('td:nth-child(4) a::text').extract_first()
        race['trainer_no_3'] = totals.css('td:nth-child(5) a::text').extract_first()
        race['trainer_no_4_below'] = totals.css('td:nth-child(6) a::text').extract_first()
        race['trainer_no_turf_races'] = totals.css('td:nth-child(13) a::text').extract_first()
        race['trainer_no_turf_wins'] = totals.css('td:nth-child(14) a::text').extract_first()
        race['trainer_no_dirt_races'] = totals.css('td:nth-child(15) a::text').extract_first()
        race['trainer_no_dirt_wins'] = totals.css('td:nth-child(16) a::text').extract_first()
        race['trainer_1_rate'] = totals.css('td:nth-child(17)::text').extract_first()
        race['trainer_1_2_rate'] = totals.css('td:nth-child(18)::text').extract_first()
        race['trainer_place_rate'] = totals.css('td:nth-child(19)::text').extract_first()
        race['trainer_sum_earnings'] = totals.css('td:nth-child(20)::text').extract_first()

        yield {
            'race': race,
        }
