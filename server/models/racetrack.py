from django.db import models

from server.models.base import BaseModel


class RaceTrack(BaseModel):
    name = models.CharField(max_length=255)
