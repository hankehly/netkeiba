import re


# You can call pipelines without linking them directly to an item type
class FooPipeline(object):
    def process_item(self, item, spider):
        print('***************** FOO!!')
        return item


class RacePipeline(object):
    def process_item(self, item, spider):
        # item['distance_meters'] = parse_distance_meters(item['race_header_text'])
        # item['weight_carried'] = str2int(item['weight_carried'])
        # item['post_position'] = str2int(item['post_position'])
        # item['order_of_finish'] = parse_order_of_finish(item['order_of_finish'])
        # item['finish_time'] = parse_finish_time(item['finish_time'])
        #
        # item['horse_sex'], item['horse_age'] = parse_horse_sex_age(item['horse_sex_age'])
        # item['horse_no_races'] = str2int(item['horse_no_races'])
        # item['horse_no_wins'] = str2int(item['horse_no_wins'])
        #
        # item['jockey_no_1'] = str2int(item['jockey_no_1'])
        # item['jockey_no_2'] = str2int(item['jockey_no_2'])
        # item['jockey_no_3'] = str2int(item['jockey_no_3'])
        # item['jockey_no_4_below'] = str2int(item['jockey_no_4_below'])
        # item['jockey_no_turf_wins'] = str2int(item['jockey_no_turf_wins'])
        # item['jockey_no_turf_races'] = str2int(item['jockey_no_turf_races'])
        # item['jockey_no_dirt_races'] = str2int(item['jockey_no_dirt_races'])
        # item['jockey_no_dirt_wins'] = str2int(item['jockey_no_dirt_wins'])
        # item['jockey_1_rate'] = str2float(item['jockey_1_rate'])
        # item['jockey_1_2_rate'] = str2float(item['jockey_1_2_rate'])
        # item['jockey_place_rate'] = str2float(item['jockey_place_rate'])
        # item['jockey_sum_earnings'] = str2float(item['jockey_sum_earnings'])
        #
        # item['trainer_no_1'] = str2int(item['trainer_no_1'])
        # item['trainer_no_2'] = str2int(item['trainer_no_2'])
        # item['trainer_no_3'] = str2int(item['trainer_no_3'])
        # item['trainer_no_4_below'] = str2int(item['trainer_no_4_below'])
        # item['trainer_no_turf_wins'] = str2int(item['trainer_no_turf_wins'])
        # item['trainer_no_turf_races'] = str2int(item['trainer_no_turf_races'])
        # item['trainer_no_dirt_races'] = str2int(item['trainer_no_dirt_races'])
        # item['trainer_no_dirt_wins'] = str2int(item['trainer_no_dirt_wins'])
        # item['trainer_1_rate'] = str2float(item['trainer_1_rate'])
        # item['trainer_1_2_rate'] = str2float(item['trainer_1_2_rate'])
        # item['trainer_place_rate'] = str2float(item['trainer_place_rate'])
        # item['trainer_sum_earnings'] = str2float(item['trainer_sum_earnings'])
        #
        # item['turf_condition'] = parse_turf_condition(item['race_header_text'])
        # item['dirt_condition'] = parse_dirt_condition(item['race_header_text'])
        # course_type = parse_course_type_one_hot(item['race_header_text'])
        # item['course_type_dirt'] = course_type['dirt']
        # item['course_type_turf'] = course_type['turf']
        # item['course_type_obstacle'] = course_type['obstacle']
        #
        # direction = parse_direction_one_hot(item['race_header_text'])
        # item['direction_left'] = direction['left']
        # item['direction_right'] = direction['right']
        # item['direction_straight'] = direction['straight']
        #
        # item['weather'] = parse_weather(item['race_header_text'])
        #
        # del item['horse_sex_age']
        # del item['race_header_text']

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


def parse_distance_meters(text):
    return str2int(re.search('([0-9]+)', text.split('/')[0]).group(1))


def parse_finish_time(text):
    if text is None:
        return None

    minutes, seconds = map(float, text.split(':'))
    return minutes * 60 + seconds


def parse_order_of_finish(text):
    return None if text in ['取', '中', '除'] else str2int(text)


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
