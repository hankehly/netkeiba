import re
from datetime import date

import scrapy
from scrapy.linkextractors import LinkExtractor


class RaceSpiderSpider(scrapy.Spider):
    name = 'race_spider'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']

    def parse(self, response):
        race_list_links = LinkExtractor(allow=r'\/race\/list\/[0-9]+', restrict_css='.race_calendar') \
            .extract_links(response)

        for link in race_list_links:
            yield scrapy.Request(link.url, callback=self.parse_race_list)

        prev_month_link = LinkExtractor(restrict_css='.race_calendar .rev').extract_links(response)[-1]
        yield scrapy.Request(prev_month_link.url, callback=self.parse)

    def parse_race_list(self, response):
        race_links = LinkExtractor(allow=r'\/race\/[0-9]+', restrict_css='.race_list').extract_links(response)

        for link in race_links:
            yield scrapy.Request(link.url, callback=self.parse_race)

    def parse_race(self, response):
        results = []
        for record in response.css('table[summary="レース結果"] tr:not(:first-child)'):
            gender_map = {
                '牡': 1,
                '牝': 2,
                'セ': 3
            }

            race_id = response.request.url.strip('/').split('/')[-1]
            order_of_finish = parse_order_of_finish(record)
            post_position = int(record.css('td:nth-child(2) span::text').extract_first())
            horse_number = int(record.css('td:nth-child(3)::text').extract_first())
            horse_name = record.css('td:nth-child(4) a[id^="umalink_"]::text').extract_first()
            horse_sex = gender_map.get(record.css('td:nth-child(5)::text').extract_first()[0])
            horse_age = int(record.css('td:nth-child(5)::text').extract_first()[1])
            mounted_weight = record.css('td:nth-child(6)::text').extract_first()
            finish_time = parse_finish_time(record)

            result = {
                'race_id': race_id,
                'order_of_finish': order_of_finish,
                'post_position': post_position,
                'horse_number': horse_number,
                'horse_name': horse_name,
                'horse_sex': horse_sex,
                'horse_age': horse_age,
                'mounted_weight': mounted_weight,
                'finish_time': finish_time,

                # todo: maybe add jockey attributes?
                'jockey': record.css('td:nth-child(7) a::text').extract_first(),

                # todo: find meaning of varieties
                # - 2.1/2 (float "/" integer)
                # - 3/4 (integer "/" integer)
                # - アタマ (string constant)
                # - クビ (string constant)
                # - ハナ
                # - 4 (integer)
                'margin': record.css('td:nth-child(9)::text').extract_first(),

                # todo: :nth-child(11) comes wrapped in a <diary_snap_cut> element
                # ' __tsuka': int(record.css('td:nth-child(11)::text').extract_first()),
            }

            results.append(result)

        yield {
            'title': response.css('.mainrace_data h1::text').extract_first(),
            'details': response.css('.mainrace_data h1+p span::text').extract_first(),
            'description': response.css('.mainrace_data .smalltxt::text').extract_first(),
            'results': results,
            'date': parse_race_date(response),
            'course_type': parse_course_type(response),
            'direction': parse_direction(response),
            'distance_meters': parse_distance(response),
            'weather': parse_weather(response)
        }


def parse_order_of_finish(record):
    extracted_text = record.css('td:nth-child(1)::text').extract_first()

    try:
        order = int(extracted_text)
    except ValueError:
        order = None

    return order


def parse_finish_time(record):
    finish_time_str = record.css('td:nth-child(8)::text').extract_first()

    if finish_time_str is None:
        return None

    minutes, seconds = map(float, finish_time_str.split(':'))
    return minutes * 60 + seconds


def parse_race_date(response):
    date_str = response.css('title::text').extract_first().split('|')[0].split('｜')[1].strip()
    year, month, day = _filter_empty(re.split('[年月日]', date_str))
    return date(year=int(year), month=int(month), day=int(day))


def parse_course_type(response):
    course_type_map = {
        'ダ': 'dirt',
        '芝': 'grass',
        '障害': 'damaged'  # ?
    }
    detail_text = response.css('.mainrace_data h1+p span::text').extract_first()
    return course_type_map.get(detail_text[0])


def parse_direction(response):
    direction_map = {
        '右': 'right',
        '左': 'left'
    }
    detail_text = response.css('.mainrace_data h1+p span::text').extract_first()
    return direction_map.get(detail_text[1])


def parse_distance(response):
    detail_text = response.css('.mainrace_data h1+p span::text').extract_first()
    return int(_filter_empty(re.split('\D', detail_text))[0])


def parse_weather(response):
    weather_map = {
        '曇': 'cloudy',
        '晴': 'sunny',
        '雨': 'rainy'
    }
    detail_text = response.css('.mainrace_data h1+p span::text').extract_first()
    weather_key = re.split('\xa0/\xa0', detail_text)[1].split(':')[-1].strip()
    return weather_map.get(weather_key)


def _filter_empty(l):
    return list(filter(None, l))
