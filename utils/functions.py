import json
import os
from urllib.request import urlretrieve
from zipfile import ZipFile

import pandas as pd


def fetch_data() -> pd.DataFrame:
    filename = 'netkeiba_20140101_20181101.jl'
    filename_zip = '{}.zip'.format(filename)
    if not os.path.isfile(filename):
        if not os.path.isfile(filename_zip):
            download_url = 'https://storage.googleapis.com/television-markup/{}'.format(filename_zip)
            urlretrieve(download_url, filename_zip)
        with ZipFile(filename_zip, 'r') as zf:
            zf.extractall()
        os.remove(filename_zip)
    df_jl = pd.read_json(filename, lines=True)
    dict_nested = json.loads(df_jl.to_json(orient='records'))
    return pd.io.json.json_normalize(dict_nested, sep='_')
