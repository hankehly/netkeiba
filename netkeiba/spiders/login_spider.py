import scrapy


class LoginSpider(scrapy.Spider):
    name = 'regist_netkeiba_com'
    start_urls = ['https://regist.netkeiba.com/account/?pid=login']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'login_id': 'henry.ehly@gmail.com', 'pswd': 'vbSBqWLptua2W9773hr3gm4XfhAz'},
            callback=self.after_login
        )

    def after_login(self, response):
        self.logger.debug('Logged in')
        self.logger.debug(response)
        # http://db.netkeiba.com/?pid=race_top
