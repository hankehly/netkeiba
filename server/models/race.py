from django.db import models

from server.models.base import BaseModel


class Race(BaseModel):
    UNKNOWN = 'UNKNOWN'

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
        (SAPPORO, 'Sapporo'),
        (HAKODATE, 'Hakodate'),
        (FUMA, 'Fuma'),
        (NIIGATA, 'Niigata'),
        (TOKYO, 'Tokyo'),
        (NAKAYAMA, 'Nakayama'),
        (CHUKYO, 'Chukyo'),
        (KYOTO, 'Kyoto'),
        (HANSHIN, 'Hanshin'),
        (OGURA, 'Ogura'),
        (UNKNOWN, 'Unknown'),
    )

    HORSE_AGE = 'HA'
    WEIGHT_FOR_AGE = 'WF'
    SET_WEIGHT = 'SW'
    HANDICAP = 'HC'
    IMPOST_CATEGORY_CHOICES = (
        # [馬齢] 同一年齢の馬だけのレース
        (HORSE_AGE, 'Horse age'),
        # [定量] 別定のなかでも、馬の年齢と性別を基準に定められているレース
        (WEIGHT_FOR_AGE, 'Weight for age'),
        # [別定] そのレース毎に負担重量を決定する基準が設けられているレース
        (SET_WEIGHT, 'Set weight'),
        # [ハンデ] 出走予定馬の実績や最近の状態などを考慮し
        # 各出走馬に勝つチャンスを与えるよう決められた重量を負担させるレース
        (HANDICAP, 'Handicap'),
        (UNKNOWN, 'Unknown'),
    )

    DIRT = 'DI'
    TURF = 'TF'
    OBSTACLE = 'OB'
    COURSE_TYPE_CHOICES = (
        (DIRT, 'Dirt'),
        (TURF, 'Turf'),
        (OBSTACLE, 'Obstacle'),
        (UNKNOWN, 'Unknown'),
    )

    G1 = 'G1'
    G2 = 'G2'
    G3 = 'G3'
    NOT_APPLICABLE = 'NA'
    GRADE_CHOICES = (
        (G1, 'G1'),
        (G2, 'G2'),
        (G3, 'G3'),
        (NOT_APPLICABLE, 'Not applicable'),
    )

    OPEN = 'OP'
    U1600 = 'U1600'
    U1000 = 'U1000'
    U500 = 'U500'
    MAIDEN = 'MD'
    UNRACED_MAIDEN = 'UMD'
    RACE_CLASS_CHOICES = (
        (OPEN, 'Open'),
        (U1600, 'Under 1600'),
        (U1000, 'Under 1000'),
        (U500, 'Under 500'),
        (MAIDEN, 'Maiden'),
        (UNRACED_MAIDEN, 'Unraced Maiden'),
        (UNKNOWN, 'Unknown'),
    )

    CLOUDY = 'CD'
    RAINY = 'RN'
    LIGHT_RAIN = 'LR'
    SUNNY = 'SN'
    SNOWY = 'SW'
    WEATHER_CHOICES = (
        (CLOUDY, 'Cloudy'),
        (RAINY, 'Rainy'),
        (LIGHT_RAIN, 'Light rain'),
        (SUNNY, 'Sunny'),
        (SNOWY, 'Snowy'),
        (UNKNOWN, 'Unknown'),
    )

    SLIGHTLY_HEAVY = 'SH'
    HEAVY = 'HV'
    GOOD = 'GD'
    BAD = 'BD'
    TRACK_CONDITION_CHOICES = (
        (SLIGHTLY_HEAVY, 'Slightly heavy'),
        (HEAVY, 'Heavy'),
        (GOOD, 'Good'),
        (BAD, 'Bad'),
        (UNKNOWN, 'Unknown'),
    )

    LEFT = 'LF'
    RIGHT = 'RI'
    STRAIGHT = 'ST'
    # TODO: Do you need 外? ("直線", "右","左","外")
    DIRECTION_CHOICES = (
        (LEFT, 'Left'),
        (RIGHT, 'Right'),
        (STRAIGHT, 'Straight'),
        (UNKNOWN, 'Unknown'),
    )

    key = models.CharField(max_length=255, unique=True)
    racetrack = models.CharField(max_length=255, choices=RACETRACK_CHOICES, default=UNKNOWN)
    impost_category = models.CharField(max_length=255, choices=IMPOST_CATEGORY_CHOICES, default=UNKNOWN)
    course_type = models.CharField(max_length=255, choices=COURSE_TYPE_CHOICES, default=UNKNOWN)
    distance = models.PositiveSmallIntegerField()
    number = models.PositiveSmallIntegerField()
    race_class = models.CharField(max_length=255, choices=RACE_CLASS_CHOICES, default=UNKNOWN)
    grade = models.CharField(max_length=255, choices=GRADE_CHOICES)
    datetime = models.DateTimeField()
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
