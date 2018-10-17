import scrapy


# TODO: add below info
# Medication Given / Bute and/or Lasix
# Final Odds / Final odds for this horse to win given by the track
# Track Conditions

class Race(scrapy.Item):
    weight_carried = scrapy.Field()
    post_position = scrapy.Field()
    trainer_previous_wins = scrapy.Field()
    trainer_num_races = scrapy.Field()
    course_type = scrapy.Field()
    weather = scrapy.Field()
    distance_meters = scrapy.Field()
    direction = scrapy.Field()
    race_url = scrapy.Field()

    horse_url = scrapy.Field()
    horse_sex = scrapy.Field()
    horse_age = scrapy.Field()
    horse_previous_wins = scrapy.Field()
    horse_num_races = scrapy.Field()

    jockey_url = scrapy.Field()
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

    # temporary attributes
    horse_sex_age = scrapy.Field()
    race_header_text = scrapy.Field()
