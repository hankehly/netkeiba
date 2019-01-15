import json
import logging
import os
import re

import pandas as pd
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from sklearn.externals import joblib
from twisted.internet import reactor

from trainer.pipeline import full_pipeline, prediction_keys

logger = logging.getLogger(__name__)


def _scrape_race(url):
    scrapy_settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'crawler.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    scrapy_settings.setmodule(settings_module_path, priority='project')

    race_key = re.search('[0-9]{12}', url).group()
    feed_filename = '.'.join([race_key, 'json'])
    feed_dir = os.path.join(settings.BASE_DIR, 'tmp', 'predict', 'data')
    feed_uri = os.path.join(feed_dir, feed_filename)

    os.makedirs(feed_dir, exist_ok=True)

    if os.path.exists(feed_uri):
        os.remove(feed_uri)

    custom_settings = {'FEED_URI': feed_uri, 'FEED_FORMAT': 'json'}
    runner = CrawlerRunner({**scrapy_settings, **custom_settings})
    d = runner.crawl('race', url)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    return json.load(open(feed_uri, 'r'))


class Command(BaseCommand):
    help = 'Predict the outcome of a race'

    def add_arguments(self, parser):
        parser.add_argument('race-url', help='The URL of the netkeiba race')
        parser.add_argument('model-path', help='The path to the prediction model')

    def handle(self, *args, **options):
        start = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        logger.info(f'Started predict command at {start}')

        race_url = options['race-url']
        model_path = options['model-path']

        if not os.path.isfile(model_path):
            raise CommandError(f'{model_path} does not exist')

        race_key = re.search('[0-9]{12}', race_url).group()
        scraped_data = _scrape_race(race_url)
        df = pd.DataFrame(scraped_data)

        X_train = df[prediction_keys]
        output_cols = ['c_post_position', 'c_horse_number', 'h_name', 'h_sex', 'c_weight_carried',
                       'j_key', 't_key', 'c_horse_weight', 'c_horse_weight_diff', 'c_first_place_odds']
        X_out = df.copy()[output_cols]

        X_train_prep = full_pipeline.fit_transform(X_train)
        estimator = joblib.load(model_path)
        X_out['c_meters_per_second'] = estimator.predict(X_train_prep)
        X_out_fmt = X_out.sort_values(by='c_meters_per_second')

        output_dir = os.path.join(settings.BASE_DIR, 'tmp', 'predict', 'results')
        os.makedirs(output_dir, exist_ok=True)

        output_file = '.'.join([race_key, 'csv'])
        output_uri = os.path.join(output_dir, output_file)
        X_out_fmt.to_csv(output_uri)

        finish = datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        duration = str(timedelta(seconds=round((finish - start).seconds)))
        logger.info(f'Finished predict command at {finish} ({duration})')
