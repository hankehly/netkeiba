from django.db import models

from server.models import BaseModel


class TrackConditionCategory(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class DirtConditionCategory(TrackConditionCategory):
    class Meta:
        db_table = 'dirt_condition_categories'


class TurfConditionCategory(TrackConditionCategory):
    class Meta:
        db_table = 'turf_condition_categories'
