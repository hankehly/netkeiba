# netkeiba

A reusable Django app which crawls and imports race data from netkeiba.com

### Installation
1. Install with pip
```bash
pip install netkeiba
```
2. Add to your existing django project
```
# settings.py
INSTALLED_APPS = [
    ...
    'netkeiba'
]
```
You should now be able to use netkeiba commands and models.

### Usage
Extract and import all data from races between 2018-01-01 ~ 2019-01-01
```bash
python manage.py pipeline --min-date 2018-01-01 --max-date 2019-01-01
```
