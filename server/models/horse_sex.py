from django.db import models

from server.models.base import BaseModel


class HorseSex(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'horse_sexes'
