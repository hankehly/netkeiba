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
    return values
    # value = values[0]
    # return re.search('([0-9]+)', value.split('/')[0]).group(1)


def parse_weight_carried(values):
    return map(int, values)


def parse_jockey_url(values):
    # jockey_href = record.css('td:nth-child(7) a::attr(href)').extract_first()
    # jockey_href_split = list(filter(None, jockey_href.split('/')))
    # jockey_href_split.insert(1, 'result')
    # jockey_href = '/' + '/'.join(jockey_href_split)
    # race['jockey'] = response.urljoin(jockey_href)
    return values


def parse_trainer_url(values):
    # trainer_url_selector = f'.race_table_01 tr:nth-child({i})'
    # trainer_url_str = LinkExtractor(allow=r'\/trainer\/[0-9]+', restrict_css=trainer_url_selector) \
    #     .extract_links(response)[0].url
    # trainer_url = urlparse(trainer_url_str)
    # trainer_id = re.match(r'/trainer/([0-9]+)/', trainer_url.path).group(1)
    # trainer_result_url = trainer_url._replace(path=f'/trainer/result/{trainer_id}')
    # race['trainer'] = urlunparse(trainer_result_url)
    return values
