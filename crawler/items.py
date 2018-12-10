import scrapy


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
