from django.db import models

from server.models.base import BaseModel


class Horse(BaseModel):
    key = models.CharField()