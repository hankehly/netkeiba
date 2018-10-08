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
