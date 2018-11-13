import json
import os
import pickle
import tempfile
from urllib.request import urlretrieve
from zipfile import ZipFile

import pandas as pd

column_rename_map = {
    'race_finisher_direction': 'direction',
    'race_finisher_distance_meters': 'distance',  # meters
    'race_finisher_finish_time_seconds': 'finish_time',  # seconds
    'race_finisher_first_place_odds': 'odds',
    'race_finisher_horse_age': 'horse_age',
    'race_finisher_horse_sex': 'horse_sex',
    'race_finisher_horse_url': 'horse_url',
    'race_finisher_horse_weight': 'horse_weight',
    'race_finisher_jockey_url': 'jockey_url',
    'race_finisher_order_of_finish': 'order_of_finish',
    'race_finisher_participant_count': 'participant_count',
    'race_finisher_popularity': 'popularity',
    'race_finisher_post_position': 'post_position',
    'race_finisher_race_date': 'date',
    'race_finisher_race_location': 'location',
    'race_finisher_race_url': 'race_url',
    'race_finisher_track_condition': 'track_condition',
    'race_finisher_track_type': 'track_type',
    'race_finisher_trainer_url': 'trainer_url',
    'race_finisher_weather': 'weather',
    'race_finisher_weight_carried': 'weight_carried'
}


def fetch_data(cache=True) -> pd.DataFrame:
    tempdir = tempfile.gettempdir()
    filename_jl = 'netkeiba_20140101_20181101.jl'
    filename_pkl = 'data.pkl'
    if not os.path.isfile(filename_pkl):
        download_url = 'https://storage.googleapis.com/television-markup/{}.zip'.format(filename_jl)
        urlretrieve(download_url, os.path.join(tempdir, '{}.zip'.format(filename_jl)))
        with ZipFile(os.path.join(tempdir, '{}.zip'.format(filename_jl)), 'r') as zf:
            zf.extractall(path=tempdir)
            os.remove(os.path.join(tempdir, '{}.zip'.format(filename_jl)))
    df_from_jsonlines = pd.read_json(os.path.join(tempdir, filename_jl), lines=True)
    data_as_dict = json.loads(df_from_jsonlines.to_json(orient='records'))
    df_normalized = pd.io.json.json_normalize(data_as_dict, sep='_')
    df = df_normalized.rename(index=str, columns=column_rename_map)
    if cache:
        pickle.dump(df, open(filename_pkl, 'wb'))
    return df
