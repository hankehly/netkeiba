# netkeiba

A scrapy project for extracting data from netkeiba.com

### Extracted data

| Feature | Description |
|:-- |:-- |
| race_finisher.weight carried | The weight carried by the horse during the race <[斤量](http://jra.jp/kouza/yougo/w229.html)> |
| race_finisher.post_position |  |
| race_finisher.order_of_finish | <[着順](http://jra.jp/kouza/yougo/w274.html)> |
| race_finisher.finish_time_seconds | <[枠番](https://www.oddspark.com/keiba/glossary/keyword/wa/42538.html)> |
| race_finisher.distance_meters | Track length in meters |
| race_finisher.weather | The weather during the race (categories limited to "sunny", "rainy" and "cloudy") |
| race_finisher.direction | (WIP) |
| race_finisher.track_condition | The physical condition of the race track (categories limited to "good", "slightly heavy", "heavy" and "bad") <馬場状態> |
| race_finisher.track_type | The type of race track (categories limited to "dirt", "turf" and "obstacle") |
| race_finisher.race_url | |
| race_finisher.horse_url | |
| race_finisher.jockey_url | |
| race_finisher.trainer_url | |
| race_finisher.participant_count | |
| race_finisher.race_date | |
| race_finisher.race_location | |
| horse.total_races | |
| horse.total_wins | |
| horse.sex | Sex of the horse (categories limited to "male", "female" and "castrated") |
| horse.age | Age of horse |
| horse.rating | User rating of horse (nullable) |
| jockey.num_1_place | Total number of times this jockey has placed 1st in a race |
| jockey.num_2_place | Total number of times this jockey has placed 2nd in a race |
| jockey.num_3_place | Total number of times this jockey has placed 3rd in a race |
| jockey.num_4_below | Total number of times this jockey has placed 4th or lower in a race |
| jockey.num_turf_races | Total number of turf races in which this jockey has participated |
| jockey.num_turf_wins | Total number of turf races this jockey has won |
| jockey.num_dirt_races | Total number of dirt races in which this jockey has participated |
| jockey.num_dirt_wins | Total number of dirt races this jockey has won |
| jockey.place_1_rate | (勝率) １着に入った割合 |
| jockey.place_1_or_2_rate | (連対率) ２着以内に入った割合 |
| jockey.place_any_rate | (複勝率) 複勝馬券が絡んだ割合 |
| jockey.sum_earnings | |
| trainer.num_1_place | Total number of times this trainer has placed 1st in a race |
| trainer.num_2_place | Total number of times this trainer has placed 2nd in a race |
| trainer.num_3_place | Total number of times this trainer has placed 3rd in a race |
| trainer.num_4_below | Total number of times this trainer has placed 4th or lower in a race |
| trainer.num_turf_races | |
| trainer.num_turf_wins | |
| trainer.num_dirt_races | |
| trainer.num_dirt_wins | |
| trainer.place_1_rate | (勝率) １着に入った割合 |
| trainer.place_1_or_2_rate | (連対率) ２着以内に入った割合 |
| trainer.place_any_rate | (複勝率) 複勝馬券が絡んだ割合 |
| trainer.sum_earnings | |

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

