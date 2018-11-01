import re
from datetime import datetime, date
from typing import List, Dict, Union, Optional

from bs4 import BeautifulSoup


def parse_horse_sex(values: List) -> Optional[str]:
    # values: ['牝2']
    possible_inputs = {
        '牡': 'male',
        '牝': 'female',
        'セ': 'castrated'
    }

    for key, val in possible_inputs.items():
        if re.search(key, values[0]):
            return val

    return None


def parse_horse_age(values: List) -> Optional[int]:
    # values: ['牝2']
    match = re.search('([0-9]+)', values[0])
    if match is None:
        return None
    return int(match.group(1))


def parse_horse_total_races(values: List) -> Optional[int]:
    # values: ['26戦4勝 [']
    match = re.search('([0-9]+)戦', values[0])
    if match is None:
        return None
    return int(match.group(1))


def parse_horse_total_wins(values: List) -> Optional[int]:
    # values: ['26戦4勝 [']
    match = re.search('([0-9]+)勝', values[0])
    if match is None:
        return None
    return int(match.group(1))


def parse_weather(values: List) -> Optional[str]:
    weather_text = values[0].split('/')[1]

    weather = {
        '曇': 'cloudy',
        '晴': 'sunny',
        '雨': 'rainy'
    }

    for key, val in weather.items():
        if f'天候 : {key}' in weather_text:
            return val

    return None


def parse_horse_url(values: List) -> str:
    return f'http://db.netkeiba.com{values[0]}'


def parse_distance_meters(values: List) -> Optional[int]:
    value = values[0] if values else None
    
    if value is None:
        return None
    
    return int(re.search('([0-9]+)', value.split('/')[0]).group(1))


def parse_post_position(values: List) -> Optional[int]:
    value = values[0] if values else None
    
    if value is None:
        return None
    
    return int(value)


def parse_order_of_finish(values: List) -> Optional[Union[int, str]]:
    # Possible values: '7', '6(降)', '取', '中', '除', '失'
    place = values[0] if values else None

    # if place is None:
    #     return None
    #
    # if place in ['取', '中', '除', '失']:
    #     return 'disqualified'
    #
    # return int(place)

    return place


def parse_finish_time_seconds(values: List) -> Optional[float]:
    text = values[0] if values else None

    if text is None:
        return None

    minutes, seconds = map(float, text.split(':'))
    return minutes * 60 + seconds


def parse_jockey_url(values: List) -> Optional[str]:
    jockey_href = values[0] if values else None
    
    if jockey_href is None:
        return None
        
    jockey_href_split = list(filter(None, jockey_href.split('/')))
    jockey_href_split.insert(1, 'result')
    jockey_href = '/'.join(jockey_href_split)
    return f'http://db.netkeiba.com/{jockey_href}'


def parse_trainer_url(values: List, loader_context: Dict) -> Optional[str]:
    tr = values[0] if values else None
    
    if tr is None:
        return None
    
    soup = BeautifulSoup(tr, 'html.parser')
    href = soup.find(href=re.compile('trainer/[0-9]+')).get('href')

    href_split = href.split('/')
    for i in range(len(href_split)):
        if href_split[i] == 'trainer':
            href_split.insert(i + 1, 'result')
            break

    href_result = '/'.join(href_split)

    return loader_context.get('response').urljoin(href_result)


def parse_direction(values: List) -> Optional[str]:
    direction_text = values[0].split('/')[0]

    directions = {
        '右': 'right',
        '左': 'left',
        '直線': 'straight'
    }

    for key, val in directions.items():
        if key in direction_text:
            return val

    return None


def str2int(values: List) -> Optional[int]:
    value = values[0] if values else None
    
    if value is None:
        return None
    
    return int(value.replace(',', ''))


def str2float(values: List) -> Optional[float]:
    value = values[0] if values else None
    
    if value is None:
        return None
    
    return float(value.replace(',', ''))


def parse_track_condition(values: List) -> Optional[str]:
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

    return None


def parse_track_type(values: List) -> Optional[str]:
    track_type_text = values[0].split('/')[0]

    track_types = {
        'ダ': 'dirt',
        '芝': 'turf',
        '障': 'obstacle'
    }

    for key, val in track_types.items():
        if key in track_type_text:
            return val

    return None


def parse_race_date(values: List) -> Optional[date]:
    # values: ['2018年9月17日 4回中山5日目 障害3歳以上未勝利\xa0\xa0(混)(定量)']
    date_str = re.search('([0-9]+)年([0-9]+)月([0-9]+)日', values[0])

    if date_str:
        year = int(date_str.group(1))
        month = int(date_str.group(2))
        day = int(date_str.group(3))
        return datetime(year, month, day).date()

    return None


def parse_race_location(values: List) -> Optional[str]:
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

    return None
