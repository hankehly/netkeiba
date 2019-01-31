from django.db import models

from server.models.base import BaseModel


class Race(BaseModel):
    UNKNOWN = 'UNKNOWN'

    # TODO: Why do you have to shorten these? Wouldn't it be easier to know what they mean automatically?
    SAPPORO = 'SP'
    HAKODATE = 'HD'
    FUMA = 'FM'
    NIIGATA = 'NG'
    TOKYO = 'TK'
    NAKAYAMA = 'NY'
    CHUKYO = 'CK'
    KYOTO = 'KT'
    HANSHIN = 'HS'
    OGURA = 'OG'
    RACETRACK_CHOICES = (
        (SAPPORO, 'sapporo'),
        (HAKODATE, 'hakodate'),
        (FUMA, 'fuma'),
        (NIIGATA, 'niigata'),
        (TOKYO, 'tokyo'),
        (NAKAYAMA, 'nakayama'),
        (CHUKYO, 'chukyo'),
        (KYOTO, 'kyoto'),
        (HANSHIN, 'hanshin'),
        (OGURA, 'ogura'),
        (UNKNOWN, 'unknown'),
    )

    HORSE_AGE = 'HA'
    WEIGHT_FOR_AGE = 'WF'
    SET_WEIGHT = 'SW'
    HANDICAP = 'HC'
    IMPOST_CATEGORY_CHOICES = (
        # [馬齢] 同一年齢の馬だけのレース
        (HORSE_AGE, 'horse_age'),
        # [定量] 別定のなかでも、馬の年齢と性別を基準に定められているレース
        (WEIGHT_FOR_AGE, 'weight_for_age'),
        # [別定] そのレース毎に負担重量を決定する基準が設けられているレース
        (SET_WEIGHT, 'set_weight'),
        # [ハンデ] 出走予定馬の実績や最近の状態などを考慮し
        # 各出走馬に勝つチャンスを与えるよう決められた重量を負担させるレース
        (HANDICAP, 'handicap'),
        (UNKNOWN, 'unknown'),
    )

    DIRT = 'DT'
    TURF = 'TF'
    OBSTACLE = 'OB'
    COURSE_TYPE_CHOICES = (
        (DIRT, 'dirt'),
        (TURF, 'turf'),
        (OBSTACLE, 'obstacle'),
        (UNKNOWN, 'unknown'),
    )

    G1 = 'G1'
    G2 = 'G2'
    G3 = 'G3'
    OP = 'OP'
    U1600 = 'U1600'
    U1000 = 'U1000'
    U500 = 'U500'
    MAIDEN = 'MD'
    UNRACED_MAIDEN = 'UMD'
    CLASS_CHOICES = (
        (G1, 'G1'),
        (G2, 'G2'),
        (G3, 'G3'),
        (OP, 'open'),
        (U1600, 'under_1600'),
        (U1000, 'under_1000'),
        (U500, 'under_500'),
        (MAIDEN, 'maiden'),
        (UNRACED_MAIDEN, 'unraced_maiden'),
        (UNKNOWN, 'unknown'),
    )

    CLOUDY = 'CD'
    RAINY = 'RN'
    LIGHT_RAIN = 'LR'
    SUNNY = 'SN'
    SNOWY = 'SW'
    WEATHER_CHOICES = (
        (CLOUDY, 'cloudy'),
        (RAINY, 'rainy'),
        (LIGHT_RAIN, 'light_rain'),
        (SUNNY, 'sunny'),
        (SNOWY, 'snowy'),
        (UNKNOWN, 'unknown'),
    )

    SLIGHTLY_HEAVY = 'SH'
    HEAVY = 'HV'
    GOOD = 'GD'
    BAD = 'BD'
    TRACK_CONDITION_CHOICES = (
        (SLIGHTLY_HEAVY, 'slightly_heavy'),
        (HEAVY, 'heavy'),
        (GOOD, 'good'),
        (BAD, 'bad'),
        (UNKNOWN, 'unknown'),
    )

    LEFT = 'LF'
    RIGHT = 'RI'
    STRAIGHT = 'ST'
    DIRECTION_CHOICES = (
        (LEFT, 'left'),
        (RIGHT, 'right'),
        (STRAIGHT, 'straight'),
        (UNKNOWN, 'unknown'),
    )

    key = models.CharField(max_length=255, unique=True)
    racetrack = models.CharField(max_length=255, choices=RACETRACK_CHOICES, default=UNKNOWN)
    impost_category = models.CharField(max_length=255, choices=IMPOST_CATEGORY_CHOICES, default=UNKNOWN)
    course_type = models.CharField(max_length=255, choices=COURSE_TYPE_CHOICES, default=UNKNOWN)
    distance = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()
    race_class = models.CharField(max_length=255, choices=CLASS_CHOICES, default=UNKNOWN)
    datetime = models.DateTimeField(null=True)
    weather = models.CharField(max_length=255, choices=WEATHER_CHOICES, default=UNKNOWN)
    track_condition = models.CharField(max_length=255, choices=TRACK_CONDITION_CHOICES, default=UNKNOWN)
    direction = models.CharField(max_length=255, choices=DIRECTION_CHOICES, default=UNKNOWN)

    # (指定) [地]が出走できるレースで、かつ地方競馬所属の騎手が騎乗できる(特指)以外のレース
    is_non_winner_regional_horse_race = models.BooleanField(default=False)

    # (特指) JRAが認定した地方競馬の競走で第1着となった[地]が出走できるレースで、かつ地方競馬所属の騎手が騎乗できるレース
    is_winner_regional_horse_race = models.BooleanField(default=False)

    # [指定] 地方競馬所属の騎手が騎乗できるレース
    is_regional_jockey_race = models.BooleanField(default=False)

    # (混合) 内国産馬にマル外が混合して出走できるレース
    is_foreign_horse_race = models.BooleanField(default=False)

    # (国際) 内国産馬に(外)および[外]が混合して出走できるレース
    is_foreign_trainer_horse_race = models.BooleanField(default=False)

    # (見習騎手) 若手騎手が騎乗できるレース
    is_apprentice_jockey_race = models.BooleanField(default=False)

    # (牝) 牝馬しか出走できないレース
    is_female_only_race = models.BooleanField(default=False)

    class Meta:
        db_table = 'races'
        get_latest_by = '-datetime'
