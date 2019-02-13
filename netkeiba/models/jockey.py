from django.db import models

from netkeiba.models.base import BaseModel


class Jockey(BaseModel):
    key = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'jockeys'
