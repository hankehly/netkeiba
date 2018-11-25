import os
from datetime import datetime
import argparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main(opts):
    jobdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'jobs')

    if not os.path.isdir(jobdir):
        os.mkdir(jobdir)

    iso_timestamp = datetime.now().isoformat(timespec='seconds')

    job_path = os.path.join(jobdir, iso_timestamp)
    os.mkdir(job_path)

    custom_settings = {
        'MIN_RACE_DATE': opts.min_race_date,
        'JOBDIR': job_path,
        'LOG_FILE': os.path.join(job_path, 'race_spider.log'),
        'FEED_URI': os.path.join(job_path, 'race_spider.jl'),
        'FEED_FORMAT': 'jsonlines',
    }

    process = CrawlerProcess({**get_project_settings(), **custom_settings})
    process.crawl('race')
    process.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--min-race-date', type=str, help='minimum race date <YYYY-MM-DD>', default='2018-01-01')
    args = parser.parse_args()
    main(args)
