import re
from datetime import datetime, date, timedelta
from typing import List

from scrapy.link import Link
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from crawler.items import WebPageItem


class DBV2Spider(CrawlSpider):
    name = 'dbv2'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']

    rules = (
        Rule(LinkExtractor(allow=[
            '/race/list/[0-9]+',
            'pid=race_top&date=[0-9]+'
        ]), process_links='process_date_links'),

        Rule(LinkExtractor(allow=[
            '/race/[0-9]+',
            '/horse/[0-9]+',
            '/trainer/[0-9]+',
            '/trainer/result/[0-9]+',
            '/trainer/profile/[0-9]+',
            '/jockey/[0-9]+',
            '/jockey/result/[0-9]+',
            '/jockey/profile/[0-9]+',
        ]), callback='parse_web_page_item'),
    )

    def __init__(self, min_race_date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if min_race_date:
            self.min_race_date = datetime.strptime(min_race_date, '%Y%m%d').date()
        else:
            self.min_race_date = date.today() - timedelta(days=30)

    def process_date_links(self, links: List[Link]):
        follow_links = []
        for link in links:
            date_string = re.search('[0-9]{8}', link.url).group()
            link_date = datetime.strptime(date_string, '%Y%m%d').date()
            if link_date >= self.min_race_date:
                follow_links.append(link)
            else:
                self.logger.info(f'Skipping url ({link.url}), {link_date} < {self.min_race_date}')
        return links

    def parse_web_page_item(self, response):
        return WebPageItem(url=response.url, html=response.text)
