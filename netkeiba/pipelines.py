from scrapy.exceptions import DropItem


class RacePipeline(object):
    def process_item(self, item, spider):
        if not item['horse'].get('total_wins'):
            item['horse']['total_wins'] = 0

        order_of_finish = item['race_finisher'].get('order_of_finish')
        finish_time_seconds = item['race_finisher'].get('finish_time_seconds')

        if order_of_finish != 'disqualified' and finish_time_seconds is None:
            raise DropItem(f'Missing race_finisher.finish_time_seconds in {item}')

        return item
