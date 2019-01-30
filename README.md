# netkeiba

A python project for scraping and analyzing horse racing data from [netkeiba.com](http://www.netkeiba.com/).

This project consists of 4 major parts:
1. Crawling
1. Scraping & Importing
1. Training & Prediction

### Crawling

The `crawler` package contains scrapy code for gathering webpage data.
HTML is stored inside a central database alongside its' urls and request fingerprint.

### Scraping & Importing

The `server` package contains logic for parsing and importing unorganized webpage data into a database with a clean schema.
The database table schema was built to facilitate easy data selection for model training; so it does not Rather than fully normalizing the schema by separating boolean / enum columns into separate tables.

### Training & prediction

The `trainer` package uses data from the previous 2 steps to train a machine learning model and predict future race outcomes. 
