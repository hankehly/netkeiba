import argparse
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings

from sklearn.externals import joblib
from tabulate import tabulate
from twisted.internet import reactor

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
from trainer.pipeline import full_pipeline, category_keys, bool_attrs, date_attributes, required_numeric_attributes, \
    nullable_numeric_attributes


def read_data(data) -> pd.DataFrame:
    df = pd.DataFrame(data)

    attrs = np.hstack([
        category_keys,
        bool_attrs,
        date_attributes,
        required_numeric_attributes,
        nullable_numeric_attributes,
        'h_key'
    ])

    return df[attrs]


def scrape(url):
    scrapy_settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'crawler.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    scrapy_settings.setmodule(settings_module_path, priority='project')
    race_key = re.search('id=c([0-9]+)', url).group(1)
    feed_filename = '.'.join([race_key, 'json'])
    feed_uri = os.path.join(PROJECT_ROOT, 'tmp', feed_filename)
    if os.path.exists(feed_uri):
        os.remove(feed_uri)
    custom_settings = {'FEED_URI': feed_uri, 'FEED_FORMAT': 'json'}
    runner = CrawlerRunner({**scrapy_settings, **custom_settings})
    d = runner.crawl('race', url)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    return json.load(open(feed_uri, 'r')), feed_uri


def main(url, model_path):
    data, feed_uri = scrape(url)
    X_train = read_data(data)
    X_out = X_train.copy()[['h_key', 'c_first_place_odds', 'c_popularity']]
    X_out['h_key'] = X_out['h_key'].astype(str)

    X_train.drop(columns=['h_key'], inplace=True)
    X_train_prep = full_pipeline.fit_transform(X_train)

    estimator = joblib.load(model_path)
    predictions = estimator.predict(X_train_prep)
    X_out['c_meters_per_second'] = predictions
    X_out.sort_values(by='c_meters_per_second', inplace=True)

    filename, _ = os.path.splitext(os.path.basename(feed_uri))
    with open(f'pred_{filename}.txt', 'w') as fh:
        print(tabulate(X_out, headers='keys', tablefmt='pipe'), file=fh)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, help='URL of the race to predict')
    parser.add_argument('model_path', type=str, help='Path to the prediction model')
    args = parser.parse_args()

    if not os.path.isfile(args.model_path):
        raise FileNotFoundError(f'model_path file does not exist: {args.model_path}')

    main(args.url, args.model_path)
