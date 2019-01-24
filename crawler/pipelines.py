from crawler.items import WebPageItem
from server.models.webpage import WebPage


class DjangoPipeline:
    def process_item(self, item, spider):
        if isinstance(item, WebPageItem):
            WebPage.objects.update_or_create(fingerprint=item['fingerprint'], defaults={
                'html': item['html'],
                'url': item['url'],
                'crawled_at': item['crawled_at']
            })
        return item
