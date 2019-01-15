from django.db import models

from server.models.base import BaseModel


class Horse(BaseModel):
    key = models.CharField(max_length=255)
    total_races = models.PositiveSmallIntegerField(null=True)
    total_wins = models.PositiveSmallIntegerField(null=True)
    birthday = models.DateField(null=True)
    sex = models.ForeignKey('HorseSex', on_delete=models.CASCADE, null=True)
    user_rating = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'horses'
