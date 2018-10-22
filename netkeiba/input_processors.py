import re
from datetime import datetime
from typing import List, Dict, Union

from bs4 import BeautifulSoup


def parse_horse_sex(values: List) -> str:
    # values: ['現役\u3000牝5歳\u3000鹿毛'] or ['抹消　牡　青鹿毛']
    age_sex_str = re.split('\s', values[0])[1]

    possible_inputs = {
        '牡': 'male',
        '牝': 'female',
        'セ': 'castrated'
    }

    for key, val in possible_inputs.items():
        if re.search(key, age_sex_str):
            return val

    return 'unknown'


def parse_horse_age(values: List):
    # values: ['現役\u3000牝5歳\u3000鹿毛'] or ['抹消　牡　青鹿毛']
    age_sex_str = re.split('\s', values[0])[1]
    match = re.search('([0-9]+)', age_sex_str)
    if match is None:
        return None
    return int(match.group(1))


def parse_horse_total_races(values: List):
    # values: ['26戦4勝 [']
    total_races_str = re.search('([0-9]+)戦', values[0]).group(1)
    return int(total_races_str)


def parse_horse_total_wins(values: List):
    # values: ['26戦4勝 [']
    total_wins_str = re.search('([0-9]+)勝', values[0]).group(1)
    return int(total_wins_str)


def parse_weather(values: List) -> str:
    weather_text = values[0].split('/')[1]

    weather = {
        '曇': 'cloudy',
        '晴': 'sunny',
        '雨': 'rainy'
    }

    for key, val in weather.items():
        if f'天候 : {key}' in weather_text:
            return val

    return 'unknown'


def parse_horse_url(values: List) -> str:
    return f'http://db.netkeiba.com{values[0]}'


def parse_distance_meters(values: List) -> int:
    return int(re.search('([0-9]+)', values[0].split('/')[0]).group(1))


def parse_post_position(values: List) -> int:
    return int(values[0])


def parse_order_of_finish(values: List) -> Union[int, str]:
    place = values[0]
    return 'disqualified' if place in ['取', '中', '除'] else int(place)


def parse_finish_time_seconds(values: List):
    text = values[0] if values else None

    if text is None:
        return None

    minutes, seconds = map(float, text.split(':'))
    return minutes * 60 + seconds


def parse_jockey_url(values: List):
    jockey_href = values[0]
    jockey_href_split = list(filter(None, jockey_href.split('/')))
    jockey_href_split.insert(1, 'result')
    jockey_href = '/'.join(jockey_href_split)
    return f'http://db.netkeiba.com/{jockey_href}'


def parse_trainer_url(values: List, loader_context: Dict):
    tr = values[0]
    soup = BeautifulSoup(tr, 'html.parser')
    href = soup.find(href=re.compile('trainer/[0-9]+')).get('href')

    href_split = href.split('/')
    for i in range(len(href_split)):
        if href_split[i] == 'trainer':
            href_split.insert(i + 1, 'result')
            break

    href_result = '/'.join(href_split)

    return loader_context.get('response').urljoin(href_result)


def parse_direction(values: List) -> str:
    direction_text = values[0].split('/')[0]

    directions = {
        '右': 'right',
        '左': 'left',
        '直線': 'straight'
    }

    for key, val in directions.items():
        if key in direction_text:
            return val

    return 'unknown'


def str2int(values: List) -> int:
    return int(values[0].replace(',', '')) if values else None


def str2float(values: List) -> float:
    return float(values[0].replace(',', '')) if values else None


def parse_track_condition(values: List) -> str:
    track_condition_text = values[0].split('/')[2]

    # TODO: Handle following case
    # 障芝 ダート2970m / 天候 : 晴 / 芝 : 良  ダート : 稍重 / 発走 : 11:20
    track_conditions = {
        '良': 'good',
        '稍重': 'slightly_heavy',
        '重': 'heavy',
        '不良': 'bad'
    }

    for key, val in track_conditions.items():
        if key in track_condition_text:
            return val

    return 'unknown'


def parse_track_type(values: List) -> str:
    track_type_text = values[0].split('/')[0]

    track_types = {
        'ダ': 'dirt',
        '芝': 'turf',
        '障': 'obstacle'
    }

    for key, val in track_types.items():
        if key in track_type_text:
            return val

    return 'unknown'


def parse_race_date(values: List):
    # values: ['2018年9月17日 4回中山5日目 障害3歳以上未勝利\xa0\xa0(混)(定量)']
    date_str = re.search('([0-9]+)年([0-9]+)月([0-9]+)日', values[0])

    if date_str:
        year = int(date_str.group(1))
        month = int(date_str.group(2))
        day = int(date_str.group(3))
        return datetime(year, month, day).date()

    return None


def parse_race_location(values: List):
    # values: ['2018年9月17日 4回中山5日目 障害3歳以上未勝利\xa0\xa0(混)(定量)']

    locations = {
        '札幌': 'sapporo',
        '函館': 'hakodate',
        '福島': 'fuma',
        '新潟': 'niigata',
        '東京': 'tokyo',
        '中山': 'nakayama',
        '中京': 'chukyo',
        '京都': 'kyoto',
        '阪神': 'hanshin',
        '小倉': 'ogura',
    }

    for key, val in locations.items():
        if re.search(key, values[0]):
            return val

    return 'unknown'
