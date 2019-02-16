# netkeiba

A Django app which crawls and imports race data from netkeiba.com

### Installation
```bash
pip install netkeiba
```

### Usage
Extract all data from races between 2018-01-01 ~ 2019-01-01
```bash
python manage.py pipeline --min-date 2018-01-01 --max-date 2019-01-01
```
