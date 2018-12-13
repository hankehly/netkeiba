import scrapy


class WebPageItem(scrapy.Item):
    url = scrapy.Field()
    html = scrapy.Field()

    def __repr__(self):
        html = f"{self['html'][:40]}... (truncated)" if len(self['html']) > 55 else self['html']
        return repr({'url': self['url'], 'html': html})
