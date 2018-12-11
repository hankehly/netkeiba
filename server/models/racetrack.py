from django.db import models

from server.models.base import BaseModel


class Race(BaseModel):
    name = models.CharField(max_length=255)
