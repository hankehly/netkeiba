from django.db import models

from server.models.base import BaseModel


class Owner(BaseModel):
    key = models.CharField(max_length=255)

    class Meta:
        db_table = 'owners'
