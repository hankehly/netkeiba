from django.db import models

from netkeiba.models.base import BaseModel


class Horse(BaseModel):
    UNKNOWN = 'UNKNOWN'
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    CASTRATED = 'CASTRATED'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (CASTRATED, 'Castrated'),
        (UNKNOWN, 'Unknown')
    )

    key = models.CharField(max_length=255, unique=True)
    age = models.PositiveSmallIntegerField(null=True)
    sex = models.CharField(max_length=255, choices=SEX_CHOICES, default=UNKNOWN)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'horses'
