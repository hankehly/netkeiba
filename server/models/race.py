from django.db import models

from server.models.base import BaseModel


class NonWinnerRegionalHorseRace(BaseModel):
    """
    (指定) [地]が出走できるレースで、かつ地方競馬所属の騎手が騎乗できる(特指)以外のレース
    http://www.jra.go.jp/kouza/keiba/
    """
    race = models.ForeignKey('Race', on_delete=models.CASCADE)

    class Meta:
        db_table = 'non_winner_regional_horse_races'


class WinnerRegionalHorseRace(BaseModel):
    """
    (特指) JRAが認定した地方競馬の競走で第1着となった[地]が出走できるレースで、かつ地方競馬所属の騎手が騎乗できるレース
    http://www.jra.go.jp/kouza/keiba/
    """
    race = models.ForeignKey('Race', on_delete=models.CASCADE)

    class Meta:
        db_table = 'winner_regional_horse_races'


class RegionalJockeyRace(BaseModel):
    """
    [指定] 地方競馬所属の騎手が騎乗できるレース
    http://www.jra.go.jp/kouza/keiba/
    """
    race = models.ForeignKey('Race', on_delete=models.CASCADE)

    class Meta:
        db_table = 'regional_jockey_races'


class ForeignHorseRace(BaseModel):
    """
    (混合) 内国産馬にマル外が混合して出走できるレース
    http://www.jra.go.jp/kouza/keiba/
    """
    race = models.ForeignKey('Race', on_delete=models.CASCADE)

    class Meta:
        db_table = 'foreign_horse_races'


class ForeignTrainerHorseRace(BaseModel):
    """
    (国際) 内国産馬に(外)および[外]が混合して出走できるレース
    http://www.jra.go.jp/kouza/keiba/
    """
    race = models.ForeignKey('Race', on_delete=models.CASCADE)

    class Meta:
        db_table = 'foreign_trainer_horse_races'


class ApprenticeJockeyRace(BaseModel):
    """
    (見習騎手) 若手騎手が騎乗できるレース
    http://www.jra.go.jp/kouza/keiba/
    """
    race = models.ForeignKey('Race', on_delete=models.CASCADE)

    class Meta:
        db_table = 'apprentice_jockey_races'


class FemaleOnlyRace(BaseModel):
    """
    (牝) 牝馬しか出走できないレース
    http://www.jra.go.jp/kouza/keiba/
    """
    race = models.ForeignKey('Race', on_delete=models.CASCADE)

    class Meta:
        db_table = 'female_only_races'


class Race(BaseModel):
    key = models.CharField(max_length=255, unique=True)
    racetrack = models.ForeignKey('Racetrack', on_delete=models.CASCADE)
    impost_category = models.ForeignKey('ImpostCategory', on_delete=models.CASCADE)
    course_type = models.ForeignKey('CourseType', on_delete=models.CASCADE)
    distance = models.PositiveSmallIntegerField()
    date = models.DateField()
    weather = models.ForeignKey('WeatherCategory', on_delete=models.CASCADE)
    turf_condition = models.ForeignKey('TurfConditionCategory', on_delete=models.CASCADE, null=True)
    dirt_condition = models.ForeignKey('DirtConditionCategory', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'races'
        get_latest_by = '-date'
