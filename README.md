# netkeiba

A scrapy project for extracting data from netkeiba.com

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
| 馬場状態 | Track condition | |


#### Example usage
```bash
scrapy crawl race_spider -o output.json [-s RACE_MIN_DATE='2018-10-14']
```

#### Example output
```json
{
    "race_finisher": {
        "weight_carried": 55.0,
        "post_position": 7,
        "order_of_finish": 5,
        "finish_time_seconds": 113.8,
        "distance_meters": 1800,
        "weather": "sunny",
        "direction": "right",
        "track_condition": "good",
        "track_type": "dirt",
        "race_url": "http://db.netkeiba.com/race/201808040504/",
        "horse_url": "http://db.netkeiba.com/horse/2015101380/",
        "jockey_url": "http://db.netkeiba.com/jockey/result/01093",
        "trainer_url": "http://db.netkeiba.com/trainer/result/01071/",
        "participant_count": 8,
        "race_date": "2018-10-14",
        "race_location": "kyoto"
    },
    "horse": {
        "total_races": 8,
        "total_wins": 1,
        "sex": "male",
        "age": 3,
        "rating": 3.59
    },
    "jockey": {
        "num_1_place": 723,
        "num_2_place": 711,
        "num_3_place": 754,
        "num_4_below": 6649,
        "num_turf_races": 4562,
        "num_turf_wins": 369,
        "num_dirt_races": 4275,
        "num_dirt_wins": 354,
        "place_1_rate": 0.082,
        "place_1_or_2_rate": 0.162,
        "place_any_rate": 0.248,
        "sum_earnings": 1453511.7
    },
    "trainer": {
        "num_1_place": 620,
        "num_2_place": 477,
        "num_3_place": 405,
        "num_4_below": 2563,
        "num_turf_races": 2596,
        "num_turf_wins": 410,
        "num_dirt_races": 1453,
        "num_dirt_wins": 207,
        "place_1_rate": 0.153,
        "place_1_or_2_rate": 0.27,
        "place_any_rate": 0.369,
        "sum_earnings": 1800019.6
    }
}
```

