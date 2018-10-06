import os

import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login_spider'
    start_urls = ['https://regist.netkeiba.com/account/?pid=login']

    def parse(self, response):
        username = os.environ.get('LOGIN_USERNAME')
        password = os.environ.get('LOGIN_PASSWORD')

        return scrapy.FormRequest.from_response(
            response,
            formdata={'login_id': username, 'pswd': password},
            formxpath='//*[@id="contents"]/div[1]/div[1]/div[2]/form',
            callback=self.after_login
        )

    def after_login(self, response):
        self.logger.debug('Logged in')
        self.logger.debug(response)

