from django.db import models

from server.models.base import BaseModel


class Horse(BaseModel):
    key = models.CharField(max_length=255)
    total_races = models.PositiveSmallIntegerField()
    total_wins = models.PositiveSmallIntegerField()
    birthday = models.DateField()
    sex = models.ForeignKey('HorseSex', on_delete=models.PROTECT)
    user_rating = models.FloatField(blank=True, null=True)
