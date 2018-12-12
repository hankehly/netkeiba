import scrapy


class WebPageItem(scrapy.Item):
    url = scrapy.Field()
    html = scrapy.Field()

    def __repr__(self):
        html = f"{self['html'][:40]}... (truncated)" if len(self['html']) > 55 else self['html']
        return repr({'url': self['url'], 'html': html})


class PageItem(scrapy.Item):
    key = scrapy.Field()
    html = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()


class Race(PageItem):
    """
    Ex. http://db.netkeiba.com/race/201806050103/
    """
    pass


class Horse(PageItem):
    """
    Ex. http://db.netkeiba.com/horse/2016105200/
    """
    pass


class TrainerResult(PageItem):
    """
    Ex. http://db.netkeiba.com/trainer/result/01059/
    """
    pass


class JockeyResult(PageItem):
    """
    Ex. http://db.netkeiba.com/jockey/result/05509/
    """
    pass
