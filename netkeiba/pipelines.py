import re


class RacePipeline(object):
    def process_item(self, item, spider):
        item['horse_sex'], item['horse_age'] = parse_horse_sex_age(item['horse_sex_age'])
        item['distance_meters'] = _filter_empty(re.split('\D', item['race_header_text']))[0]
        item['weight_carried'] = str2int(item['weight_carried'])
        item['horse_age'] = str2int(item['horse_age'])
        item['post_position'] = str2int(item['post_position'])
        item['order_of_finish'] = str2int(item['order_of_finish'])
        item['horse_no_races'] = str2int(item['horse_no_races'])
        item['horse_previous_wins'] = str2int(item['horse_previous_wins'])
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

        del item['horse_sex_age']
        del item['race_header_text']

        return item


def str2int(val):
    return int(val.replace(',', ''))


def str2float(val):
    return float(val.replace(',', ''))


# TODO: It can be multiple of these
def parse_course_type(response):
    course_type_map = {
        'ダ': 'dirt',
        '芝': 'turf',
        '障害': 'obstacle'
    }
    # detail_text = response.css('.mainrace_data h1+p span::text').extract_first()
    # matches = [v for k, v in course_type_map.items() if re.search(k, detail_text)]
    # return matches[0] if matches else None
    return None


# TODO: You need to work on this
def parse_direction(response):
    direction_map = {
        '右': 'right',
        '左': 'left',
        '直線': 'straight'
    }
    # detail_text = response.css('.mainrace_data h1+p span::text').extract_first()
    # matches = [v for k, v in direction_map.items() if re.search(k, detail_text)]
    # return matches[0] if matches else None
    return None


def parse_weather(response):
    weather_map = {
        '曇': 'cloudy',
        '晴': 'sunny',
        '雨': 'rainy',
        '小雨': 'drizzle'
    }
    detail_text = response.css('.mainrace_data h1+p span::text').extract_first()
    weather_key = re.split('\xa0/\xa0', detail_text)[1].split(':')[-1].strip()
    return weather_map.get(weather_key)


def parse_horse_sex_age(text):
    gender_map = {
        '牡': 'male',
        '牝': 'female',
        'セ': 'castrated'
    }
    return gender_map.get(text[0]), text[1]


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
