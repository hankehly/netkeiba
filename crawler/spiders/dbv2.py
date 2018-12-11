from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from crawler.items import WebPageItem


class DBV2Spider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']

    rules = (
        Rule(LinkExtractor(allow=['/race/list/[0-9]+'])),

        Rule(LinkExtractor(allow=[
            '/race/[0-9]+',
            '/horse/[0-9]+',
            '/trainer/[0-9]+',
            '/trainer/result/[0-9]+',
            '/trainer/profile/[0-9]+',
            '/jockey/[0-9]+',
            '/jockey/result/[0-9]+',
            '/jockey/profile/[0-9]+',
            'http://db.netkeiba.com//?pid=race_board&thread=race&id=201809050204'
        ]), callback='parse'),
    )

    # You can also get a list of comments for a specific race via the following API
    # curl 'https://bbs.netkeiba.com/?pid=api_get_comment_list&sort=1&key=201809050204&max_length=1000&limit=20&page=1&category_cd=race' | jq
    #
    # {
    #     "status": "OK",
    #     "data": {
    #         "count": "56",
    #         "list": [
    #             {
    #                 "comment_id": "56",
    #                 "sns_user_id": "8531617",
    #                 "avatar_url": "http://img.findfriends.jp/profile/17/8531617_4.jpg?746",
    #                 "user_url": "http://user.netkeiba.com?pid=user_prof&id=8531617",
    #                 "nickname": "ﾏｻｷﾝ☆",
    #                 "comment": ">>54\nいま見ました\n単でしたね(T ^ T)",
    #                 "like_count": "0",
    #                 "is_hidden_comment": "0",
    #                 "is_anonymous": "0",
    #                 "is_update": "0",
    #                 "datetime": "2018/12/2 12:10",
    #                 "like_comment": "99",
    #                 "hidden_comment": "99",
    #                 "delete_comment": "0",
    #                 "follow_tag": "<a href=\"https://regist.netkeiba.com/account?pid=login&service=s01\"><span><span class=\"Btn\"><span class=\"Icon Icon_Follow\"></span>フォローする</span></span></a>"
    #             },
    # you should also checkout keibalist because it looks easier to parse and has easy to read data-bunseki stuff
    def parse(self, response):
        return WebPageItem(url=response.url, html=response.text)
