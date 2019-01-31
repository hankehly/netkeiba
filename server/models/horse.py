from django.db import models

from server.models.base import BaseModel


class Horse(BaseModel):
    UNKNOWN = 'UNKNOWN'
    MALE = 'ML'
    FEMALE = 'FM'
    CASTRATED = 'CT'
    SEX_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female'),
        (CASTRATED, 'castrated'),
        (UNKNOWN, 'unknown')
    )

    key = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(null=True)
    sex = models.CharField(max_length=255, choices=SEX_CHOICES, default=UNKNOWN)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'horses'
