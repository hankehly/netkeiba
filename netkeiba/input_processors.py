from typing import List, Union, Optional


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


def parse_first_place_odds(values: List) -> Optional[float]:
    value = values[0] if values else None

    if value is None or value == '---':
        return None

    return float(value)
