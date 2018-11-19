import scrapy


class BaseRequestItem(scrapy.Item):
    item_type = scrapy.Field()
    id = scrapy.Field()
    response_body = scrapy.Field()
    url = scrapy.Field()


class RaceRequest(BaseRequestItem):
    pass


class HorseRequest(BaseRequestItem):
    pass


class TrainerRequest(BaseRequestItem):
    pass


class JockeyRequest(BaseRequestItem):
    pass
