import re


class RacePipeline(object):
    def process_item(self, item, spider):
        return item


def str2int(val):
    return int(val.replace(',', ''))


def str2float(val):
    return float(val.replace(',', ''))


def parse_course_type_one_hot(text):
    course_types = {
        'dirt': 0,
        'turf': 0,
        'obstacle': 0
    }

    if re.search(r'ダ', text):
        course_types['dirt'] = 1
    if re.search(r'芝', text):
        course_types['turf'] = 1
    if re.search(r'障', text):
        course_types['obstacle'] = 1

    return course_types


def parse_direction_one_hot(text):
    directions = {
        'right': 0,
        'left': 0,
        'straight': 0
    }

    if re.search(r'右', text):
        directions['right'] = 1
    if re.search(r'左', text):
        directions['left'] = 1
    if re.search(r'直線', text):
        directions['straight'] = 1

    return directions


def parse_weather(text):
    weather_text = text.split('/')[1]

    weather = {
        '曇': 'cloudy',
        '晴': 'sunny',
        '雨': 'rainy'
    }

    for key, val in weather.items():
        if f'天候 : {key}' in weather_text:
            return val

    return None


def parse_turf_condition(text):
    condition_text = text.split('/')[2]

    conditions = {
        '芝 : 良': 'good',
        '芝 : 稍重': 'slightly_heavy',
        '芝 : 重': 'heavy',
        '芝 : 不良': 'bad'
    }

    for key, val in conditions.items():
        if f': {key}' in condition_text:
            return val

    return None


def parse_dirt_condition(text):
    condition_text = text.split('/')[2]

    conditions = {
        'ダート : 良': 'good',
        'ダート : 稍重': 'slightly_heavy',
        'ダート : 重': 'heavy',
        'ダート : 不良': 'bad'
    }

    for key, val in conditions.items():
        if f': {key}' in condition_text:
            return val

    return None

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
