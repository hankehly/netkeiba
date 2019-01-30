# netkeiba

The aim of this project it to equip you with everything needed to predict race outcomes in Japanese horse races. It consists of 3 major parts:
1. Crawling
1. Scraping & Importing
1. Training & Prediction

### 1. Crawling

The `crawler` package contains scrapy code for gathering webpage data.
HTML is stored inside a central database alongside its' urls and request fingerprint.

### 2. Scraping & Importing

The `server` package contains logic for parsing and importing unorganized webpage data into a database with a clean schema.
The database table schema was built to facilitate easy data selection for model training; so it does not go as far as normalizing boolean / enum columns into separate tables.

### 3. Training & prediction

The `trainer` package uses data from the previous 2 steps to train a machine learning model and predict future race outcomes. 
