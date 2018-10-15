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
    "course_type": "dirt",
    "weather": "cloudy",
    "distance_meters": 1400,
    "direction": "right",
    "weight_carried": "57",
    "horse_sex": 1,
    "horse_age": 5,
    "post_position": 2,
    "order_of_finish": 15,
    "race_url": "http://db.netkeiba.com/race/201809040712/",
    "horse_profile": "http://db.netkeiba.com/horse/2013104817/",
    "jockey_record": "http://db.netkeiba.com/jockey/result/01139",
    "horse_num_races": "<tr>\n<th>\u901a\u7b97\u6210\u7e3e</th>\n<td>24",
    "horse_previous_wins": "3",
    "jockey_no_1": "60",
    "jockey_no_2": "63",
    "jockey_no_3": "60",
    "jockey_no_4_below": "1,074",
    "jockey_no_grass_races": "389",
    "jockey_no_grass_wins": "13",
    "jockey_no_dirt_races": "594",
    "jockey_no_dirt_wins": "14",
    "jockey_1_rate": ".048",
    "jockey_1_2_rate": ".098",
    "jockey_place_rate": ".146",
    "jockey_sum_earnings": "127,464.9"
}
```
