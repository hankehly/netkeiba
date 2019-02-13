from django.db import models

from netkeiba.models.base import BaseModel


class Trainer(BaseModel):
    UNKNOWN = 'UNKNOWN'

    EAST = 'EAST'
    WEST = 'WEST'
    REGIONAL = 'REGIONAL'
    OVERSEAS = 'OVERSEAS'
    STABLE_CHOICES = (
        (EAST, 'East'),
        (WEST, 'West'),
        (REGIONAL, 'Regional'),
        (OVERSEAS, 'Overseas'),
        (UNKNOWN, 'Unknown')
    )

    key = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    stable = models.CharField(max_length=255, choices=STABLE_CHOICES, default=UNKNOWN)

    class Meta:
        db_table = 'trainers'
