import re


class RacePipeline(object):
    def process_item(self, item, spider):
        # output to pandas dataframe with normalized json structure
        # data = json.load(open('output.json', 'rb'))
        # df = pd.io.json.json_normalize(data, sep='_')

        # drop items with no finish time
        return item

# arr = [
# 'ダ右1400m / 天候 : 晴 / ダート : 稍重 / 発走 : 09:55',
# '芝左1400m / 天候 : 晴 / 芝 : 良 / 発走 : 11:10',
# '芝左1800m / 天候 : 晴 / 芝 : 良 / 発走 : 15:45',
# '芝左1600m / 天候 : 晴 / 芝 : 良 / 発走 : 14:35',
# 'ダ右1400m / 天候 : 晴 / ダート : 稍重 / 発走 : 11:25',
# 'ダ右1200m / 天候 : 雨 / ダート : 稍重 / 発走 : 10:40',
# 'ダ右1800m / 天候 : 曇 / ダート : 稍重 / 発走 : 15:35',
# '芝右 外2200m / 天候 : 曇 / 芝 : 良 / 発走 : 15:45',
# 'ダ右1200m / 天候 : 曇 / ダート : 稍重 / 発走 : 14:40',
# 'ダ右1800m / 天候 : 晴 / ダート : 重 / 発走 : 11:10'
# '障芝 ダート2880m / 天候 : 晴 / 芝 : 良  ダート : 良 / 発走 : 11:40',
# '障芝3110m / 天候 : 晴 / 芝 : 稍重 / 発走 : 14:15'
# ]

# ['ダ右1400m ', ' 天候 : 晴 ', ' ダート : 稍重 ', ' 発走 : 11:25']
