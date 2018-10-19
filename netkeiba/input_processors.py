import re


def parse_horse_sex(values):
    value = re.split('[戦勝]', values[0])[:2]

    possible_inputs = {
        '牡': 'male',
        '牝': 'female',
        'セ': 'castrated'
    }

    return possible_inputs.get(value[0])


def parse_horse_age(values):
    value = re.split('[戦勝]', values[0])[:2]

    return int(value[1])


def parse_horse_url(values):
    return f'http://db.netkeiba.com{values[0]}'


def parse_distance_meters(values):
    return int(re.search('([0-9]+)', values[0].split('/')[0]).group(1))


def parse_weight_carried(values):
    return int(values[0])


def parse_post_position(values):
    return int(values[0])


def parse_order_of_finish(values):
    text = values[0]
    return None if text in ['取', '中', '除'] else int(text)


def parse_finish_time(values):
    text = values[0]

    if text is None:
        return None

    minutes, seconds = map(float, text.split(':'))
    return minutes * 60 + seconds


def parse_jockey_url(values):
    jockey_href = values[0]
    jockey_href_split = list(filter(None, jockey_href.split('/')))
    jockey_href_split.insert(1, 'result')
    jockey_href = '/'.join(jockey_href_split)
    return f'http://db.netkeiba.com/{jockey_href}'


def parse_trainer_url(values):
    # trainer_url_selector = f'.race_table_01 tr:nth-child({i})'
    # trainer_url_str = LinkExtractor(allow=r'\/trainer\/[0-9]+', restrict_css=trainer_url_selector) \
    #     .extract_links(response)[0].url
    # trainer_url = urlparse(trainer_url_str)
    # trainer_id = re.match(r'/trainer/([0-9]+)/', trainer_url.path).group(1)
    # trainer_result_url = trainer_url._replace(path=f'/trainer/result/{trainer_id}')
    # race['trainer'] = urlunparse(trainer_result_url)
    return values
