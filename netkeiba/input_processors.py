import re
from typing import List, Optional, Dict

from bs4 import BeautifulSoup


def parse_horse_sex(values: List) -> str:
    # '現役\u3000牝5歳\u3000鹿毛'
    value = re.split('\s', values[0])[1]

    possible_inputs = {
        '牡': 'male',
        '牝': 'female',
        'セ': 'castrated'
    }

    return possible_inputs.get(value)


def parse_horse_age(values: List) -> int:
    return values
    # '現役\u3000牝5歳\u3000鹿毛'
    # value = re.split('\s', values[0])[1]
    # return int(value)


def parse_horse_rating(values: List):
    return values


def parse_horse_total_races(values: List):
    return values


def parse_horse_total_wins(values: List) -> float:
    return values
    # return float(values[0]) if values else None


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


def parse_distance_meters(values: List) -> int:
    return int(re.search('([0-9]+)', values[0].split('/')[0]).group(1))


def parse_weight_carried(values: List) -> int:
    return int(values[0])


def parse_post_position(values: List) -> int:
    return int(values[0])


def parse_order_of_finish(values: List) -> Optional[int]:
    text = values[0]
    return None if text in ['取', '中', '除'] else int(text)


def parse_finish_time(values: List):
    text = values[0]

    if text is None:
        return None

    minutes, seconds = map(float, text.split(':'))
    return minutes * 60 + seconds


def parse_jockey_url(values: List, loader_context: Dict):
    jockey_href = values[0]
    jockey_href_split = list(filter(None, jockey_href.split('/')))
    jockey_href_split.insert(1, 'result')
    jockey_href = '/'.join(jockey_href_split)
    return loader_context.get('response').urljoin(jockey_href)


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


def parse_direction(values: List) -> Optional[str]:
    direction_text = values[0].split('/')[0]

    directions = {
        '右': 'right',
        '左': 'left',
        '直線': 'straight'
    }

    for key, val in directions.items():
        if f'天候 : {key}' in direction_text:
            return val

    return None
