import scrapy


class BaseWebPageItem(scrapy.Item):
    url = scrapy.Field()
    html = scrapy.Field()
    fingerprint = scrapy.Field()

    def __repr__(self):
        html = f"{self['html'][:40]}... (truncated)" if len(self['html']) > 55 else self['html']
        return repr({'url': self['url'], 'html': html})


# TODO: Rename this class and model to be specific to Netkeiba (ie. NetkeibaWebPageItem)
class WebPageItem(BaseWebPageItem):
    pass


class JMAWebPageItem(BaseWebPageItem):
    pass
