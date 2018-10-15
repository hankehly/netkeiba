import scrapy


# TODO: add below info
# Medication Given / Bute and/or Lasix
# Final Odds / Final odds for this horse to win given by the track
# Track Conditions

class Race(scrapy.Item):
    weight_carried = scrapy.Field()
    horse_sex = scrapy.Field()
    horse_age = scrapy.Field()
    post_position = scrapy.Field()
    horse_previous_wins = scrapy.Field()  # (通算成績: 12戦"1勝")
    horse_num_races = scrapy.Field()  # (通算成績: "12戦"1勝)
    jockey_previous_wins = scrapy.Field()
    jockey_num_races = scrapy.Field()
    trainer_previous_wins = scrapy.Field()
    trainer_num_races = scrapy.Field()
    course_type = scrapy.Field()
    weather = scrapy.Field()
    distance_meters = scrapy.Field()
    direction = scrapy.Field()
    race_url = scrapy.Field()
    horse_profile = scrapy.Field()
    jockey_record = scrapy.Field()
    order_of_finish = scrapy.Field()
    jockey_win_rate = scrapy.Field()
