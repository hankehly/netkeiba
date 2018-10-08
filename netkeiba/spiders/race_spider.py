import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class RaceSpiderSpider(CrawlSpider):
    name = 'race_spider'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']

    rules = (
        Rule(LinkExtractor(allow=r'pid=race_top&date=[0-9]+')),
        Rule(LinkExtractor(allow=r'\/race\/list\/[0-9]+\/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response)
        i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
