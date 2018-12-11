from django.db import models

from server.models.base import BaseModel


class HorseSex(BaseModel):
    key = models.CharField(max_length=255)
