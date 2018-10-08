import scrapy
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
        for i, record in enumerate(response.css('table[summary="レース結果"] tr')):
            if i == 0:
                continue
            yield {
                'horse_name': record.css('a[id^="umalink_"]::text').extract_first()
            }
