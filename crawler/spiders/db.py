import re
from datetime import datetime, date, timedelta
from typing import List

from scrapy.link import Link
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.request import request_fingerprint

from crawler.items import WebPageItem


class DBSpider(CrawlSpider):
    name = 'db'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['https://db.netkeiba.com/?pid=race_top']

    rules = (
        Rule(LinkExtractor(allow=['/race/list/[0-9]+', 'pid=race_top&date=[0-9]+']),
             process_links='process_date_links'),

        Rule(LinkExtractor(allow='/race/[0-9]+', restrict_css='.race_list'), callback='parse_web_page_item',
             follow=True),

        Rule(LinkExtractor(allow=[
            '/horse/[0-9]+',
            '/trainer/[0-9]+',
            '/jockey/[0-9]+',
        ], restrict_css='#db_race_detail .race_table_01'), callback='parse_web_page_item', follow=True),

        Rule(LinkExtractor(allow=[
            '/trainer/result/[0-9]+',
            '/jockey/result/[0-9]+',
            '/trainer/profile/[0-9]+',
            '/jockey/profile/[0-9]+',
        ], restrict_css='#horse_detail .db_detail_menu'), callback='parse_web_page_item')
    )

    def __init__(self, min_date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if min_date:
            self.min_date = datetime.strptime(min_date, '%Y-%m-%d').date()
        else:
            self.min_date = date.today() - timedelta(days=30)

        self.logger.info(f'min_date set to {self.min_date}')

    def process_date_links(self, links: List[Link]):
        follow_links = []
        for link in links:
            date_string = re.search('[0-9]{8}', link.url).group()
            link_date = datetime.strptime(date_string, '%Y%m%d').date()

            is_race_top_page = 'pid=race_top' in link.url
            is_valid_month = link_date.month >= self.min_date.month
            is_valid_date = link_date >= self.min_date

            if is_valid_date or (is_race_top_page and is_valid_month):
                follow_links.append(link)
            else:
                self.logger.info(f'Skipping url ({link.url}), {link_date} < {self.min_date}')
        return follow_links

    def parse_web_page_item(self, response):
        fingerprint = request_fingerprint(response.request)
        return WebPageItem(url=response.url, html=response.text, fingerprint=fingerprint)
