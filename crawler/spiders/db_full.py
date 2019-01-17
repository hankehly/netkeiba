from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from crawler.items import WebPageItem


class DBFullSpider(CrawlSpider):
    name = 'db_full'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['https://db.netkeiba.com/']

    rules = [
        Rule(LinkExtractor(), callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        return WebPageItem.from_response(response)
