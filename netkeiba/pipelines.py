import re


class RacePipeline(object):
    def process_item(self, item, spider):
        item['distance_meters'] = parse_distance_meters(item['race_header_text'])
        item['weight_carried'] = str2int(item['weight_carried'])
        item['post_position'] = str2int(item['post_position'])
        item['order_of_finish'] = str2int(item['order_of_finish'])

        item['horse_sex'], item['horse_age'] = parse_horse_sex_age(item['horse_sex_age'])
        item['horse_no_races'] = str2int(item['horse_no_races'])
        item['horse_no_wins'] = str2int(item['horse_no_wins'])

        item['jockey_no_1'] = str2int(item['jockey_no_1'])
        item['jockey_no_2'] = str2int(item['jockey_no_2'])
        item['jockey_no_3'] = str2int(item['jockey_no_3'])
        item['jockey_no_4_below'] = str2int(item['jockey_no_4_below'])
        item['jockey_no_turf_wins'] = str2int(item['jockey_no_turf_wins'])
        item['jockey_no_turf_races'] = str2int(item['jockey_no_turf_races'])
        item['jockey_no_dirt_races'] = str2int(item['jockey_no_dirt_races'])
        item['jockey_no_dirt_wins'] = str2int(item['jockey_no_dirt_wins'])
        item['jockey_1_rate'] = str2float(item['jockey_1_rate'])
        item['jockey_1_2_rate'] = str2float(item['jockey_1_2_rate'])
        item['jockey_place_rate'] = str2float(item['jockey_place_rate'])
        item['jockey_sum_earnings'] = str2float(item['jockey_sum_earnings'])

        item['trainer_no_1'] = str2int(item['trainer_no_1'])
        item['trainer_no_2'] = str2int(item['trainer_no_2'])
        item['trainer_no_3'] = str2int(item['trainer_no_3'])
        item['trainer_no_4_below'] = str2int(item['trainer_no_4_below'])
        item['trainer_no_turf_wins'] = str2int(item['trainer_no_turf_wins'])
        item['trainer_no_turf_races'] = str2int(item['trainer_no_turf_races'])
        item['trainer_no_dirt_races'] = str2int(item['trainer_no_dirt_races'])
        item['trainer_no_dirt_wins'] = str2int(item['trainer_no_dirt_wins'])
        item['trainer_1_rate'] = str2float(item['trainer_1_rate'])
        item['trainer_1_2_rate'] = str2float(item['trainer_1_2_rate'])
        item['trainer_place_rate'] = str2float(item['trainer_place_rate'])
        item['trainer_sum_earnings'] = str2float(item['trainer_sum_earnings'])

        course_type = parse_course_type_one_hot(item['race_header_text'])
        item['course_type_dirt'] = course_type['dirt']
        item['course_type_turf'] = course_type['turf']
        item['course_type_obstacle'] = course_type['obstacle']

        direction = parse_direction_one_hot(item['race_header_text'])
        item['direction_left'] = direction['left']
        item['direction_right'] = direction['right']
        item['direction_straight'] = direction['straight']

        weather = parse_weather_one_hot(item['race_header_text'])
        item['weather_cloudy'] = weather['cloudy']
        item['weather_sunny'] = weather['sunny']
        item['weather_rainy'] = weather['rainy']

        del item['horse_sex_age']
        del item['race_header_text']

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
    if re.search(r'障害', text):
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


def parse_weather_one_hot(text):
    weather = {
        'cloudy': 0,
        'sunny': 0,
        'rainy': 0
    }

    if re.search(r'曇', text):
        weather['cloudy'] = 1
    if re.search(r'晴', text):
        weather['sunny'] = 1
    if re.search(r'雨', text):
        weather['rainy'] = 1

    return weather


def parse_horse_sex_age(text):
    gender_map = {
        '牡': 'male',
        '牝': 'female',
        'セ': 'castrated'
    }
    return gender_map.get(text[0]), str2int(text[1])


def parse_distance_meters(text):
    return str2int(_filter_empty(re.split('\D', text))[0])


def parse_finish_time(text):
    if text is None:
        return None

    minutes, seconds = map(float, text.split(':'))
    return minutes * 60 + seconds


def _filter_empty(l):
    return list(filter(None, l))

# arr = ['ダ右1400m / 天候 : 晴 / ダート : 稍重 / 発走 : 09:55',
# '芝左1400m / 天候 : 晴 / 芝 : 良 / 発走 : 11:10',
# '芝左1800m / 天候 : 晴 / 芝 : 良 / 発走 : 15:45',
# '芝左1600m / 天候 : 晴 / 芝 : 良 / 発走 : 14:35',
# 'ダ右1400m / 天候 : 晴 / ダート : 稍重 / 発走 : 11:25',
# 'ダ右1200m / 天候 : 雨 / ダート : 稍重 / 発走 : 10:40',
# 'ダ右1800m / 天候 : 曇 / ダート : 稍重 / 発走 : 15:35',
# '芝右 外2200m / 天候 : 曇 / 芝 : 良 / 発走 : 15:45',
# 'ダ右1200m / 天候 : 曇 / ダート : 稍重 / 発走 : 14:40',
# 'ダ右1800m / 天候 : 晴 / ダート : 重 / 発走 : 11:10']
