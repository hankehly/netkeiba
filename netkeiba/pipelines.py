import re


class RacePipeline(object):
    def process_item(self, item, spider):
        # output to pandas dataframe with normalized json structure
        # data = json.load(open('output.json', 'rb'))
        # df = pd.io.json.json_normalize(data, sep='_')

        # drop items with no finish time
        return item
