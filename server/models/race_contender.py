from django.db import models

from server.models import BaseModel


class RaceContender(BaseModel):
    UNKNOWN = 'UNKNOWN'

    OK = 'OK'
    DISQUALIFIED = 'DQ'  # 失
    CANCELLED = 'CL'  # 取|除
    REMOUNT = 'RM'  # 再
    DID_NOT_FINISH = 'DNF'  # 中
    POSITION_LOWERED = 'PL'  # 降
    POSITION_STATE_CHOICES = (
        (OK, 'ok'),
        (DISQUALIFIED, 'disqualified'),
        (CANCELLED, 'cancelled'),
        (REMOUNT, 'remount'),
        (DID_NOT_FINISH, 'did_not_finish'),
        (POSITION_LOWERED, 'position_lowered'),
        (UNKNOWN, 'unknown')
    )

    race = models.ForeignKey('server.Race', on_delete=models.CASCADE)
    horse = models.ForeignKey('server.Horse', on_delete=models.CASCADE)
    jockey = models.ForeignKey('server.Jockey', on_delete=models.CASCADE)
    trainer = models.ForeignKey('server.Trainer', on_delete=models.CASCADE)
    owner = models.ForeignKey('server.Owner', on_delete=models.CASCADE)
    order_of_finish = models.PositiveSmallIntegerField()
    order_of_finish_lowered = models.BooleanField()
    disqualified = models.BooleanField()
    did_remount = models.BooleanField()
    post_position = models.PositiveSmallIntegerField()
    weight_carried = models.FloatField()
    finish_time = models.FloatField()
    first_place_odds = models.FloatField()
    popularity = models.PositiveSmallIntegerField()
    horse_weight = models.FloatField(null=True)
    horse_weight_diff = models.FloatField(null=True)

    class Meta:
        db_table = 'race_contenders'
        unique_together = ('race', 'horse', 'jockey', 'trainer')
