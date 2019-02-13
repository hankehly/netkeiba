from django.db import models

from netkeiba.models.base import BaseModel


class Owner(BaseModel):
    key = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'owners'
