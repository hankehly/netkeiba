from scrapy.exceptions import DropItem


class RacePipeline(object):
    def process_item(self, item, spider):
        # output to pandas dataframe with normalized json structure
        # data = json.load(open('output.json', 'rb'))
        # df = pd.io.json.json_normalize(data, sep='_')

        if not item['race_finisher']['finish_time']:
            raise DropItem(f'Missing race_finisher.finish_time in {item}')

        return item
