from scrapy.exceptions import DropItem


class RacePipeline(object):
    def process_item(self, item, spider):
        if not item['horse'].get('total_wins'):
            item['horse']['total_wins'] = 0

        order_of_finish = item['race_finisher'].get('order_of_finish')
        finish_time = item['race_finisher'].get('finish_time')

        if order_of_finish != 'disqualified' and finish_time is None:
            raise DropItem(f'Missing race_finisher.finish_time in {item}')

        return item
