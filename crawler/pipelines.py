from crawler.items import WebPageItem
from server.models.webpage import WebPage


class DjangoPipeline:
    def process_item(self, item, spider):
        if isinstance(item, WebPageItem):
            WebPage.objects.update_or_create(url=item['url'], defaults={'html': item['html']})
        return item
