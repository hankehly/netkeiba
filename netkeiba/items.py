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
    parse_post_position,
    parse_order_of_finish,
    parse_finish_time,
    parse_horse_total_races,
    parse_horse_total_wins,
    parse_weather,
    parse_direction,
    str2int,
    str2float,
    parse_track_condition,
    parse_track_type,
    parse_race_date,
    parse_race_location
)


class RaceFinisher(scrapy.Item):
    race_url = scrapy.Field()
    horse_url = scrapy.Field(input_processor=parse_horse_url)
    jockey_url = scrapy.Field(input_processor=parse_jockey_url)
    trainer_url = scrapy.Field(input_processor=parse_trainer_url)
    weight_carried = scrapy.Field(input_processor=str2float)
    post_position = scrapy.Field(input_processor=parse_post_position)
    order_of_finish = scrapy.Field(input_processor=parse_order_of_finish)
    finish_time = scrapy.Field(input_processor=parse_finish_time)
    distance_meters = scrapy.Field(input_processor=parse_distance_meters)
    weather = scrapy.Field(input_processor=parse_weather)
    direction = scrapy.Field(input_processor=parse_direction)
    track_condition = scrapy.Field(input_processor=parse_track_condition)
    track_type = scrapy.Field(input_processor=parse_track_type)
    participant_count = scrapy.Field()
    race_date = scrapy.Field(input_processor=parse_race_date)
    race_location = scrapy.Field(input_processor=parse_race_location)


class Horse(scrapy.Item):
    sex = scrapy.Field(input_processor=parse_horse_sex)
    age = scrapy.Field(input_processor=parse_horse_age)
    rating = scrapy.Field(input_processor=str2float)
    total_races = scrapy.Field(input_processor=parse_horse_total_races)
    total_wins = scrapy.Field(input_processor=parse_horse_total_wins)


class AnnualRecordHolder(scrapy.Item):
    no_1 = scrapy.Field(input_processor=str2int)
    no_2 = scrapy.Field(input_processor=str2int)
    no_3 = scrapy.Field(input_processor=str2int)
    no_4_below = scrapy.Field(input_processor=str2int)
    no_turf_races = scrapy.Field(input_processor=str2int)
    no_turf_wins = scrapy.Field(input_processor=str2int)
    no_dirt_races = scrapy.Field(input_processor=str2int)
    no_dirt_wins = scrapy.Field(input_processor=str2int)
    place_1_rate = scrapy.Field(input_processor=str2float)
    place_1_or_2_rate = scrapy.Field(input_processor=str2float)
    place_any_rate = scrapy.Field(input_processor=str2float)
    sum_earnings = scrapy.Field(input_processor=str2float)


class Jockey(AnnualRecordHolder):
    pass


class Trainer(AnnualRecordHolder):
    pass

# class Race(scrapy.Item):
#     course_type_dirt = scrapy.Field()
#     course_type_turf = scrapy.Field()
#     course_type_obstacle = scrapy.Field()
