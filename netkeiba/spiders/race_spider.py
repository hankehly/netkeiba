from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class RaceSpiderSpider(CrawlSpider):
    name = 'race_spider'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']

    rules = (
        Rule(LinkExtractor(allow=r'pid=race_top&date=[0-9]+')),
        Rule(LinkExtractor(allow=r'\/race\/list\/[0-9]+\/')),
        Rule(LinkExtractor(allow=r'\/race\/[0-9]+'), callback='parse_item'),
    )

    def parse_item(self, response):
        results = []
        for record in response.css('table[summary="レース結果"] tr')[1:]:
            gender_map = {
                '牡': 1,
                '牝': 2,
                'セ': 3
            }

            results.append({
                'order_of_finish': int(record.css('td:nth-child(1)::text').extract_first()),
                'post_position': int(record.css('td:nth-child(2) span::text').extract_first()),
                'horse_number': int(record.css('td:nth-child(3)::text').extract_first()),
                'horse_name': record.css('td:nth-child(4) a[id^="umalink_"]::text').extract_first(),
                'sex': gender_map.get(record.css('td:nth-child(5)::text').extract_first()[0]),
                'age': int(record.css('td:nth-child(5)::text').extract_first()[1]),
                'mounted_weight': int(record.css('td:nth-child(6)::text').extract_first()),

                # todo: maybe add jockey attributes?
                'jockey': record.css('td:nth-child(7) a::text').extract_first(),

                # todo: convert to seconds
                'finish_time': record.css('td:nth-child(8)::text').extract_first(),

                # todo: find meaning of varieties
                # - 2.1/2 (float "/" integer)
                # - 3/4 (integer "/" integer)
                # - アタマ (string constant)
                # - クビ (string constant)
                # - ハナ
                # - 4 (integer)
                'margin': record.css('td:nth-child(9)::text').extract_first(),
                # todo: :nth-child(11) comes wrapped in a <diary_snap_cut> element
                # '__tsuka': int(record.css('td:nth-child(11)::text').extract_first()),
            })

        # ['3歳上1000万下', '2018年10月02日 ']
        # title_components = response.css('title::text').extract_first().split('|')[0].split('｜')

        yield {
            'title': response.css('.mainrace_data h1::text').extract_first(),
            'details': response.css('.mainrace_data h1+p span::text').extract_first(),
            'description': response.css('.mainrace_data .smalltxt::text').extract_first(),
            'results': results
        }
