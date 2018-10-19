import scrapy

from scrapy.loader.processors import Compose

# TODO: add below info
# Medication Given / Bute and/or Lasix
# Final Odds / Final odds for this horse to win given by the track
from netkeiba.input_processors import parse_horse_sex, parse_horse_age


class Horse(scrapy.Item):
    sex = scrapy.Field(
        input_processor=Compose(parse_horse_sex)
    )

    age = scrapy.Field(
        input_processor=Compose(parse_horse_age)
    )

    total_wins = scrapy.Field()
    total_races = scrapy.Field()


class Jockey(scrapy.Item):
    pass


class RaceFinish(scrapy.Item):
    pass


class Race(scrapy.Item):
    race_horse_weight_carried = scrapy.Field()
    race_horse_post_position = scrapy.Field()
    race_course_type_dirt = scrapy.Field()
    race_course_type_turf = scrapy.Field()
    race_course_type_obstacle = scrapy.Field()
    race_turf_condition = scrapy.Field()
    race_dirt_condition = scrapy.Field()
    race_weather = scrapy.Field()
    race_distance_meters = scrapy.Field()
    race_direction_left = scrapy.Field()
    race_direction_right = scrapy.Field()
    race_direction_straight = scrapy.Field()
    race_order_of_finish = scrapy.Field()
    race_finish_time = scrapy.Field()

    trainer = scrapy.Field()
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

    # url references
    race_url = scrapy.Field()
    horse = scrapy.Field()
    jockey = scrapy.Field()

    # temporary attributes
    horse_sex_age = scrapy.Field()
    race_header_text = scrapy.Field()
