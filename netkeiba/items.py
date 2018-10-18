import scrapy


# TODO: add below info
# Medication Given / Bute and/or Lasix
# Final Odds / Final odds for this horse to win given by the track
# Track Conditions

class Race(scrapy.Item):
    race_url = scrapy.Field()
    weight_carried = scrapy.Field()
    post_position = scrapy.Field()
    course_type_dirt = scrapy.Field()
    course_type_turf = scrapy.Field()
    course_type_obstacle = scrapy.Field()
    weather_cloudy = scrapy.Field()
    weather_sunny = scrapy.Field()
    weather_rainy = scrapy.Field()
    distance_meters = scrapy.Field()
    direction_left = scrapy.Field()
    direction_right = scrapy.Field()
    direction_straight = scrapy.Field()

    trainer = scrapy.Field()
    trainer_previous_wins = scrapy.Field()
    trainer_num_races = scrapy.Field()

    horse = scrapy.Field()
    horse_sex = scrapy.Field()
    horse_age = scrapy.Field()
    horse_no_wins = scrapy.Field()
    horse_no_races = scrapy.Field()

    jockey = scrapy.Field()
    jockey_num_races = scrapy.Field()
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

    order_of_finish = scrapy.Field()
    finish_time = scrapy.Field()

    # temporary attributes
    horse_sex_age = scrapy.Field()
    race_header_text = scrapy.Field()
