import scrapy

from scrapy.loader.processors import TakeFirst

# TODO: add below info
# Medication Given / Bute and/or Lasix
# Final Odds / Final odds for this horse to win given by the track
from netkeiba.input_processors import (
    parse_horse_sex,
    parse_horse_age,
    parse_jockey_url,
    parse_trainer_url,
    parse_horse_url,
    parse_distance_meters,
    parse_weight_carried
)


class Horse(scrapy.Item):
    sex = scrapy.Field(input_processor=parse_horse_sex)
    age = scrapy.Field(input_processor=parse_horse_age)
    total_wins = scrapy.Field()
    total_races = scrapy.Field()


class Jockey(scrapy.Item):
    pass


class RaceFinish(scrapy.Item):
    weight_carried = scrapy.Field(input_processor=parse_weight_carried)
    post_position = scrapy.Field()
    order_of_finish = scrapy.Field()
    finish_time = scrapy.Field()
    distance_meters = scrapy.Field(input_processor=parse_distance_meters)
    race_url = scrapy.Field()
    horse = scrapy.Field(input_processor=parse_horse_url)
    jockey = scrapy.Field(input_processor=parse_jockey_url)
    trainer = scrapy.Field(input_processor=parse_trainer_url)
    pass


class Race(scrapy.Item):
    course_type_dirt = scrapy.Field()
    course_type_turf = scrapy.Field()
    course_type_obstacle = scrapy.Field()
    turf_condition = scrapy.Field()
    dirt_condition = scrapy.Field()
    weather = scrapy.Field()
    direction_left = scrapy.Field()
    direction_right = scrapy.Field()
    direction_straight = scrapy.Field()

    trainer_win_rate = scrapy.Field()
    trainer_no_1 = scrapy.Field()
    trainer_no_2 = scrapy.Field()
    trainer_no_3 = scrapy.Field()
    trainer_no_4_below = scrapy.Field()
    trainer_no_turf_races = scrapy.Field()
    trainer_no_turf_wins = scrapy.Field()
    trainer_no_dirt_races = scrapy.Field()
    trainer_no_dirt_wins = scrapy.Field()
    trainer_1_rate = scrapy.Field()
    trainer_1_2_rate = scrapy.Field()
    trainer_place_rate = scrapy.Field()
    trainer_sum_earnings = scrapy.Field()

    jockey_win_rate = scrapy.Field()
    jockey_no_1 = scrapy.Field()
    jockey_no_2 = scrapy.Field()
    jockey_no_3 = scrapy.Field()
    jockey_no_4_below = scrapy.Field()
    jockey_no_turf_races = scrapy.Field()
    jockey_no_turf_wins = scrapy.Field()
    jockey_no_dirt_races = scrapy.Field()
    jockey_no_dirt_wins = scrapy.Field()
    jockey_1_rate = scrapy.Field()
    jockey_1_2_rate = scrapy.Field()
    jockey_place_rate = scrapy.Field()
    jockey_sum_earnings = scrapy.Field()

    # temporary attributes
    horse_sex_age = scrapy.Field()
    race_header_text = scrapy.Field()
