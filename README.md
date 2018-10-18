# netkeiba

A scrapy project for extracting race data from netkeiba.com

### Usage

Run `race_spider` crawler to scrape all race data.
```bash
scrapy crawl race_spider -o races.json
```

### Extracted data

| JP | EN | Description |
|:-- |:-- |:-- |
| 斤量　| mounted_weight(?) | 騎手の体重　＋　騎手が身につけているもの（勝負服やプロテクター）と所定の馬具（鞍など）の重量 |
| 着差 | margin | ... |
| | order_of_finish | |
| | post_position | |
| | horse_number | |
| | horse_name | |
| | sex | |
| | age | |
| | jockey | |
| | finish_time | |
| | margin | |
| 勝率 | | １着に入った割合 |
| 連対率 | | ２着以内に入った割合 |
| 複勝率 | | 複勝馬券が絡んだ割合 |

```json
{
    "weight_carried": 57,
    "post_position": 5,
    "order_of_finish": 7,
    "finish_time": 81.4,
    "race_url": "http://db.netkeiba.com/race/201809040310/",
    "horse": "http://db.netkeiba.com/horse/2014104831/",
    "jockey": "http://db.netkeiba.com/jockey/result/01014",
    "trainer": "http://db.netkeiba.com/trainer/result/01105",
    "horse_no_races": 8,
    "horse_no_wins": 2,
    "jockey_no_1": 2129,
    "jockey_no_2": 1818,
    "jockey_no_3": 1692,
    "jockey_no_4_below": 10898,
    "jockey_no_turf_races": 8867,
    "jockey_no_turf_wins": 1203,
    "jockey_no_dirt_races": 7670,
    "jockey_no_dirt_wins": 926,
    "jockey_1_rate": 0.129,
    "jockey_1_2_rate": 0.239,
    "jockey_place_rate": 0.341,
    "jockey_sum_earnings": 4415420.0,
    "trainer_no_1": 318,
    "trainer_no_2": 311,
    "trainer_no_3": 307,
    "trainer_no_4_below": 1945,
    "trainer_no_turf_races": 1880,
    "trainer_no_turf_wins": 215,
    "trainer_no_dirt_races": 990,
    "trainer_no_dirt_wins": 102,
    "trainer_1_rate": 0.11,
    "trainer_1_2_rate": 0.218,
    "trainer_place_rate": 0.325,
    "trainer_sum_earnings": 812955.6,
    "distance_meters": 1400,
    "horse_sex": "male",
    "horse_age": 4,
    "course_type_dirt": 0,
    "course_type_turf": 1,
    "course_type_obstacle": 0,
    "direction_left": 0,
    "direction_right": 1,
    "direction_straight": 0,
    "weather_cloudy": 1,
    "weather_sunny": 0,
    "weather_rainy": 0
}
```
