from inflection import underscore

from crawler.items import PageItem, WebPageItem
from server.models.webpage import WebPage


class PageTypePipeline:
    def process_item(self, item, spider):
        if isinstance(item, PageItem):
            # Set the `type` property of the item to the snake-case version of its class
            item['type'] = underscore(type(item).__name__)

        if isinstance(item, WebPageItem):
            WebPage.objects.update_or_create(url=item['url'], defaults={'html': item['html']})

        return item
