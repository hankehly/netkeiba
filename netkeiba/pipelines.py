# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# {
#     "course_type": null,
#     "weather": "cloudy",
#     "distance_meters": "1800",
#     "direction": null,
#     "weight_carried": "54",
#     "horse_sex": "male",
#     "horse_age": "3",
#     "post_position": "7",
#     "order_of_finish": "1",
#     "race_url": "http://db.netkeiba.com/race/201806040512/",
#     "horse_profile": "http://db.netkeiba.com/horse/2015104299/",
#     "jockey_record": "http://db.netkeiba.com/jockey/result/01075",
#     "horse_num_races": "4",
#     "horse_previous_wins": "2",
#     "jockey_no_1": "785",
#     "jockey_no_2": "758",
#     "jockey_no_3": "823",
#     "jockey_no_4_below": "7,469",
#     "jockey_no_turf_races": "4,888",
#     "jockey_no_turf_wins": "369",
#     "jockey_no_dirt_races": "4,947",
#     "jockey_no_dirt_wins": "416",
#     "jockey_1_rate": ".080",
#     "jockey_1_2_rate": ".157",
#     "jockey_place_rate": ".241",
#     "jockey_sum_earnings": "1,461,169.7"
# }

class RacePipeline(object):
    def process_item(self, item, spider):
        item['distance_meters'] = str2int(item['distance_meters'])
        item['weight_carried'] = str2int(item['weight_carried'])
        item['horse_age'] = str2int(item['horse_age'])
        item['post_position'] = str2int(item['post_position'])
        item['order_of_finish'] = str2int(item['order_of_finish'])
        item['horse_num_races'] = str2int(item['horse_num_races'])
        item['horse_previous_wins'] = str2int(item['horse_previous_wins'])
        item['jockey_no_1'] = str2int(item['jockey_no_1'])
        item['jockey_no_2'] = str2int(item['jockey_no_2'])
        item['jockey_no_3'] = str2int(item['jockey_no_3'])
        item['jockey_no_4_below'] = str2int(item['jockey_no_4_below'])
        item['jockey_no_turf_wins'] = str2int(item['jockey_no_turf_wins'])
        item['jockey_no_turf_races'] = str2int(item['jockey_no_turf_races'])
        item['jockey_no_dirt_races'] = str2int(item['jockey_no_dirt_races'])
        item['jockey_no_dirt_wins'] = str2int(item['jockey_no_dirt_wins'])
        item['jockey_1_rate'] = str2float(item['jockey_1_rate'])
        item['jockey_1_2_rate'] = str2float(item['jockey_1_2_rate'])
        item['jockey_place_rate'] = str2float(item['jockey_place_rate'])
        item['jockey_sum_earnings'] = str2float(item['jockey_sum_earnings'])
        return item


def str2int(val):
    return int(val.replace(',', ''))


def str2float(val):
    return float(val.replace(',', ''))
