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
    "course_type": null,
    "weather": "sunny",
    "distance_meters": 1300,
    "direction": null,
    "weight_carried": 54,
    "horse_sex": "male",
    "horse_age": 2,
    "post_position": 7,
    "order_of_finish": 12,
    "race_url": "http://db.netkeiba.com/race/201805040101/",
    "horse_profile": "http://db.netkeiba.com/horse/2016102995/",
    "jockey_record": "http://db.netkeiba.com/jockey/result/01169",
    "horse_num_races": 3,
    "horse_previous_wins": 0,
    "jockey_no_1": 57,
    "jockey_no_2": 68,
    "jockey_no_3": 68,
    "jockey_no_4_below": 899,
    "jockey_no_turf_races": 449,
    "jockey_no_turf_wins": 23,
    "jockey_no_dirt_races": 643,
    "jockey_no_dirt_wins": 34,
    "jockey_1_rate": 0.052,
    "jockey_1_2_rate": 0.114,
    "jockey_place_rate": 0.177,
    "jockey_sum_earnings": 80935.0
}
```
