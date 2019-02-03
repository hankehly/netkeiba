from django.db import models

from server.models.base import BaseModel


class Trainer(BaseModel):
    EAST = 'EAST'
    WEST = 'WEST'
    REGIONAL = 'REGIONAL'
    OVERSEAS = 'OVERSEAS'
    STABLE_CHOICES = (
        (EAST, 'East'),
        (WEST, 'West'),
        (REGIONAL, 'Regional'),
        (OVERSEAS, 'Overseas'),
    )

    key = models.CharField(max_length=255)
    stable = models.CharField(max_length=255, choices=STABLE_CHOICES)

    class Meta:
        db_table = 'trainers'
