import scrapy


from netkeiba.input_processors import (
    parse_horse_sex,
    parse_horse_age,
    parse_jockey_url,
    parse_trainer_url,
    parse_horse_url,
    parse_distance_meters,
    parse_post_position,
    parse_order_of_finish,
    parse_finish_time_seconds,
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
    finish_time_seconds = scrapy.Field(input_processor=parse_finish_time_seconds)
    distance_meters = scrapy.Field(input_processor=parse_distance_meters)
    weather = scrapy.Field(input_processor=parse_weather)
    direction = scrapy.Field(input_processor=parse_direction)
    track_condition = scrapy.Field(input_processor=parse_track_condition)
    track_type = scrapy.Field(input_processor=parse_track_type)
    participant_count = scrapy.Field()
    race_date = scrapy.Field(input_processor=parse_race_date)
    race_location = scrapy.Field(input_processor=parse_race_location)
    horse_sex = scrapy.Field(input_processor=parse_horse_sex)
    horse_age = scrapy.Field(input_processor=parse_horse_age)
    first_place_odds = scrapy.Field(input_processor=str2float)
    popularity = scrapy.Field(input_processor=str2int)
    horse_weight = scrapy.Field()


class Horse(scrapy.Item):
    rating = scrapy.Field(input_processor=str2float)
    total_races = scrapy.Field(input_processor=parse_horse_total_races)
    total_wins = scrapy.Field(input_processor=parse_horse_total_wins)


class AnnualRecordHolder(scrapy.Item):
    num_1_place = scrapy.Field(input_processor=str2int)
    num_2_place = scrapy.Field(input_processor=str2int)
    num_3_place = scrapy.Field(input_processor=str2int)
    num_4_below = scrapy.Field(input_processor=str2int)
    num_turf_races = scrapy.Field(input_processor=str2int)
    num_turf_wins = scrapy.Field(input_processor=str2int)
    num_dirt_races = scrapy.Field(input_processor=str2int)
    num_dirt_wins = scrapy.Field(input_processor=str2int)
    place_1_rate = scrapy.Field(input_processor=str2float)
    place_1_or_2_rate = scrapy.Field(input_processor=str2float)
    place_any_rate = scrapy.Field(input_processor=str2float)
    sum_earnings = scrapy.Field(input_processor=str2float)


class Jockey(AnnualRecordHolder):
    pass


class Trainer(AnnualRecordHolder):
    pass
