from django.db import models

from server.models import BaseModel


class RaceContender(BaseModel):
    race = models.ForeignKey('server.Race', on_delete=models.CASCADE)
    horse = models.ForeignKey('server.Horse', on_delete=models.CASCADE)
    jockey = models.ForeignKey('server.Jockey', on_delete=models.CASCADE)
    trainer = models.ForeignKey('server.Trainer', on_delete=models.CASCADE)
    order_of_finish = models.PositiveSmallIntegerField()
    order_of_finish_lowered = models.BooleanField()
    did_remount = models.BooleanField()
    post_position = models.PositiveSmallIntegerField()
    weight_carried = models.FloatField()
    finish_time = models.FloatField()
    first_place_odds = models.FloatField()
    popularity = models.PositiveSmallIntegerField()
    horse_weight = models.FloatField()
    horse_weight_diff = models.FloatField()

    class Meta:
        db_table = 'race_contenders'
        unique_together = ('race', 'horse', 'jockey', 'trainer')
