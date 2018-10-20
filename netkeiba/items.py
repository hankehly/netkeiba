import scrapy

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
    parse_weight_carried,
    parse_post_position,
    parse_order_of_finish,
    parse_finish_time,
    parse_horse_rating,
    parse_horse_total_races,
    parse_horse_total_wins,
    parse_weather,
    parse_direction
)


class Horse(scrapy.Item):
    sex = scrapy.Field(input_processor=parse_horse_sex)
    age = scrapy.Field(input_processor=parse_horse_age)
    rating = scrapy.Field(input_processor=parse_horse_rating)
    total_races = scrapy.Field(input_processor=parse_horse_total_races)
    total_wins = scrapy.Field(input_processor=parse_horse_total_wins)


class Jockey(scrapy.Item):
    pass


class RaceFinish(scrapy.Item):
    race_url = scrapy.Field()
    weight_carried = scrapy.Field(input_processor=parse_weight_carried)
    post_position = scrapy.Field(input_processor=parse_post_position)
    order_of_finish = scrapy.Field(input_processor=parse_order_of_finish)
    finish_time = scrapy.Field(input_processor=parse_finish_time)
    distance_meters = scrapy.Field(input_processor=parse_distance_meters)
    horse = scrapy.Field(input_processor=parse_horse_url)
    jockey = scrapy.Field(input_processor=parse_jockey_url)
    trainer = scrapy.Field(input_processor=parse_trainer_url)
    weather = scrapy.Field(input_processor=parse_weather)
    direction = scrapy.Field(input_processor=parse_direction)


class Race(scrapy.Item):
    course_type_dirt = scrapy.Field()
    course_type_turf = scrapy.Field()
    course_type_obstacle = scrapy.Field()
    turf_condition = scrapy.Field()
    dirt_condition = scrapy.Field()
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
